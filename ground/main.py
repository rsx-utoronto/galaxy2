# already installed with default python installation, no need to install manually
import sys
import os
import time 
import random
from math import *
from collections import OrderedDict

# need to install these manually
# install pyserial
import serial
# install pygame
import pygame 
#install PyQt4
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# install matplotlib
from matplotlib.backends import qt4_compat
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
# also need to install PyKDE4.marble (used in Joystick.py)

# written by us, in github repo
from PacketSerial import *
import Joystick
import SensorGetter
import GPSGui
import Graphs
import RoverTopview
import SensorSimulator
import DebugConsole


# define constants here
ARM_ADDRESS = chr(0x10)  # since pyserial likes to get them as strings. 
SENSOR_ADDRESS = chr(0x11)  # doesn't seem to be used anywhere, do we still need this?
DRIVE_ADDRESS = chr(0x12)
SENSOR_READ_ADDRESSES = [chr(0x80), chr(0x81), chr(0x82), chr(0x83), chr(0x84), chr(0x85), ]
SENSORS = [0 for i in range(16)] 

try:
    ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
    pser = PacketSerial(ser)
except:
    print "Serial connection failed: probably not plugged in"


class application_window(QMainWindow):
    def __init__(self):
        global ARM_ADDRESS, SENSOR_ADDRESS, DRIVE_ADDRESS, SENSOR_READ_ADDRESSES
        global SENSORS, ser, pser 

        QMainWindow.__init__(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")
        self.resize(1000, 1000)

        # --- Menu --- #
        self.file_menu = QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 Qt.CTRL + Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        # --- Widgets --- #
        self.tabs = QTabWidget()
        self.graph_widget = QWidget()
        self.map_widget = QWidget()
        self.topview_widget = QWidget()
        self.console_widget = QWidget()

        # Sensor graph objects
        gas_sensor = Graphs.ScrollingGraph(200, SensorSimulator.gas_sensor)
        moisture_sensor = Graphs.ScrollingGraph(200, \
            SensorSimulator.moisture_sensor)
        # possible sensors that the user can select from to graph,
        # dictionary for easy access by name
        dict_of_graphs = {'Gas Sensor':gas_sensor,\
        'Moisture Sensor':moisture_sensor}

        # Dynamic canvases to hold graphs
        dc1 = Graphs.DynamicGraphCanvas(\
            gas_sensor, dict_of_graphs, parent=self.graph_widget, width=5, height=4, dpi=100)
        dc2 = Graphs.DynamicGraphCanvas(\
            moisture_sensor, dict_of_graphs, parent=self.graph_widget, width=5, height=4, dpi=100)

        # Combo box for selecting which graphs to view
        self.graph_chooser_top = QComboBox(self.graph_widget)
        self.graph_chooser_top.addItems(['Gas Sensor', 'Moisture Sensor'])
        self.graph_chooser_bottom = QComboBox(self.graph_widget)
        self.graph_chooser_bottom.addItems(['Gas Sensor', 'Moisture Sensor'])

        # Combo box event
        self.graph_chooser_top.activated[str].connect(dc1.graph_change_handler)
        self.graph_chooser_bottom.activated[str].connect(dc2.graph_change_handler)
        self.graph_chooser_bottom.setCurrentIndex(1)      # set contents to be the graph being displayed

        # Debug console
        console = DebugConsole.DebugConsole(parent=self.console_widget)
        console.resize(self.size().width() * 0.5, self.size().height() * 0.3)

        # Make map widget
        if GPSGui.marble_imported:                    # see import statement at top for reason
            UTIAS = Marble.GeoDataCoordinates(-79.466083, 43.782247, 0, Marble.GeoDataCoordinates.Degree)
            gps_map = GPSGui.GPSMapWidget(UTIAS,'UTIASTest.osm','/dev/ttyUSB0','/dev/ttyUSB1')
        
        # Start joystick
        try:                      # so that it can still run without joystick connected
            JOYSTICK_CONNECTED = True
            self.joystick_thread = QThread()
            self.j = Joystick.Joystick(ARM_ADDRESS, DRIVE_ADDRESS, ser, pser)
            self.j.moveToThread(self.joystick_thread)

            self.connect(self.joystick_thread, SIGNAL("started()"), self.j.start_joystick)
            self.connect(self.joystick_thread, SIGNAL("finished()"), self.j.end_joystick)

            self.joystick_thread.start()
        except:
            JOYSTICK_CONNECTED = False
            print "Failed to start joystick: joystick probably not plugged in"

        # start sensor getter
        try:
            self.sensor_getter_thread = QThread()
            self.sg = SensorGetter.SensorGetter(SENSOR_READ_ADDRESSES, SENSORS, ser, pser)
            sef.sg.moveToThread(self.sensor_getter_thread)

            self.connect(self.sensor_getter_thread, SIGNAL("started()"), self.j.start_sg)
            self.connect(self.sensor_getter_thread, SIGNAL("finished()"), self.j.end_sg)

            self.sensor_getter_thread.start()
        except:
            print "Failed to start sensor getter"

        
        # Coloured wheels widget
        rov = RoverTopview.RoverTopview()

        ### Create main layouts ###
        main_layout0 = QVBoxLayout()
        top_layout1 = QHBoxLayout()
        bottom_layout1 = QHBoxLayout()
        map_layout2 = QVBoxLayout()
        joystick_layout2 = QHBoxLayout()
        debugging_layout2 = QVBoxLayout()
        graph_layout2 = QHBoxLayout()

        # Box layout for graph items, holds 2 graph canvases and combo box
        l = QHBoxLayout()
        v1 = QVBoxLayout()
        v2 = QVBoxLayout()
        v1.addWidget(dc1)
        v1.addWidget(self.graph_chooser_top)
        v2.addWidget(dc2)
        v2.addWidget(self.graph_chooser_bottom)
        l.addLayout(v1)
        l.addLayout(v2)

        # Map layout
        if GPSGui.marble_imported:    # see import for reason
            map_layout2.addWidget(gps_map)
        else:
            temp_map_label = QLabel()
            temp_map_label.setStyleSheet('QLabel {background-color: grey; color: white;}')
            temp_map_label.setText('Map goes here')
            map_layout2.addWidget(temp_map_label)

        # Joystick setting buttons
        # Allows the user to select which system is being controlled by the joystick
        jscb_layout = QHBoxLayout()
        joystick_system_control_buttons =\
            QGroupBox(QString('Which system is controlled by the joystick?'))
        self.control_arm_button = QRadioButton(QString('Robot arm'), parent=\
            joystick_system_control_buttons)
        self.control_drive_button = QRadioButton(QString('Drive system'), parent=\
            joystick_system_control_buttons)
        self.control_drive_button.setChecked(True)  # set default value
        if JOYSTICK_CONNECTED:
            self.j.joystick_control_arm_button(False)   # ensure default value set above is true
        jscb_layout.addWidget(self.control_arm_button)
        jscb_layout.addWidget(self.control_drive_button)
        joystick_system_control_buttons.setLayout(jscb_layout)
        joystick_layout2.addWidget(joystick_system_control_buttons)
        # Allows the user to select which arm joint is being controlled by the joystick
        jacb_layout = QHBoxLayout()
        joystick_arm_control_buttons =\
            QGroupBox(QString('Which arm joint is controlled by the joystick?'))
        self.joint_1_button = QRadioButton(QString('1'), parent=\
            joystick_arm_control_buttons)
        self.joint_2_button = QRadioButton(QString('2'), parent=\
            joystick_arm_control_buttons)
        self.joint_3_button = QRadioButton(QString('3'), parent=\
            joystick_arm_control_buttons)
        self.joint_1_button.setChecked(True)   # set default value
        if JOYSTICK_CONNECTED:
            self.j.joint_to_control_button(1)
        jacb_layout.addWidget(self.joint_1_button)
        jacb_layout.addWidget(self.joint_2_button)
        jacb_layout.addWidget(self.joint_3_button)
        joystick_arm_control_buttons.setLayout(jacb_layout)
        joystick_layout2.addWidget(joystick_arm_control_buttons)

        # Connect joystick settings buttons to joystick code
        if JOYSTICK_CONNECTED:
            self.control_arm_button.clicked().connect(self.j.joystick_controls_arm_button(True))
            self.control_drive_button.clicked().connect(self.j.joystick_controls_arm_button(False))
            self.j.system_to_control_changed.connect(self.system_to_control_changed)

            self.joint_1_button.clicked().connect(self.j.joint_to_control_button(1))
            self.joint_2_button.clicked().connect(self.j.joint_to_control_button(2))
            self.joint_3_button.clicked().connect(self.j.joint_to_control_button(3))
            self.j.joint_to_control_changed.connect(self.joint_to_control_changed)

        # Console layout
        debugging_layout2.addWidget(self.console_widget)

        # Print joystick state to console
        if JOYSTICK_CONNECTED:
            if self.j.joystick_controls_arm:
                console.prnt('Joystick controls arm.')
            else:
                console.prnt('Joystick controls drive system')
            console.prnt('''Arm joint being controlled (if
                joystick controls arm): ''' + str(self.j.joint_to_control))
        else:
            console.prnt('Joystick not connected.')

        # Control sizing
        top_layout1.addStrut(self.size().height() * 0.7) # set to 70% window height
        bottom_layout1.addStrut(self.size().height() * 0.3) # set to 30% window height
        map_layout2.addStrut(self.size().width() * 0.5)
        debugging_layout2.addStrut(self.size().width() * 0.5)

        # Put all of the layouts together
        main_layout0.addLayout(top_layout1)
        main_layout0.addLayout(bottom_layout1)
        top_layout1.addLayout(map_layout2)
        top_layout1.addLayout(joystick_layout2)
        bottom_layout1.addLayout(debugging_layout2)
        bottom_layout1.addLayout(graph_layout2)
        graph_layout2.addLayout(l)

        main_widget = QWidget()
        main_widget.setLayout(main_layout0)

        self.tabs.addTab(main_widget, 'Main')

        self.tabs.setWindowTitle('RSX Rover Control')
        self.tabs.show()

    def system_to_control_changed(self, joystick_controls_arm):
        if joystick_controls_arm:
            self.control_arm_button.setChecked(True)
        elif not joystick_controls_arm:
            self.control_drive_button.setChecked(False)

    def joint_to_control_changed(self, joint):
        exec('self.joint_%d_button.setChecked(True)' % joint)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()


if __name__ == "__main__":

    qApp = QApplication(sys.argv)
    qApp.setWindowIcon(QIcon('icon.png'))

    aw = application_window()
    sys.exit(qApp.exec_())
    #qApp.exec_()
