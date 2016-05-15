#install PyQt4
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class DebugTextWindow(QLabel):

    '''
    Inherits QLabel. Displays text from previously entered commands and
    output from the system.
    '''

    def __init__(self, parent=None):

        QLabel.__init__(self, parent=parent)
        # Holds the text that will be displayed
        self.text = QString()
        self.setFrameShape(QFrame.Box)
        self.setStyleSheet('''QLabel {
            background-color: white;
            font-family: freemono;
            color: black;
        }''')
        self.setAlignment(Qt.AlignTop)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setWordWrap(True)

    def update(self):
        
        self.setText(self.text)

    def prnt(self, text):
        
        self.text.append(str(text) + '\n')
        self.update()

    def clear(self):
        
        # TODO: make it so that console clears, but can still scroll up to
        # old text (currently all text gets deleted).
        self.text = QString()
        self.update()


class DebugConsoleInput(QLineEdit):
    
    def __init__(self, parent=None):
        
        QLineEdit.__init__(self, parent=parent)


class DebugConsole(QWidget):

    def __init__(self, parent=None):
        
        QWidget.__init__(self, parent=parent)

        self.scroll_area = QScrollArea()
        self.text_window = DebugTextWindow(parent=self.scroll_area)
        self.inpt = DebugConsoleInput(parent=self)

        self.inpt.returnPressed.connect(self.return_pressed_handler)

        self.scroll_area.setWidget(self.text_window)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.inpt)
        self.setLayout(self.layout)

    def prnt(self, text):

        self.text_window.prnt(text)

    def return_pressed_handler(self):
        
        '''
        Get text in QLineEdit, clear text from box and print text. Is QString.
        '''
        
        text = self.inpt.text()
        text = '> ' + text   # to make it clear where there is a new command
        self.inpt.clear()
        self.prnt(text)

        if text == '> clear':
            self.text_window.clear()
