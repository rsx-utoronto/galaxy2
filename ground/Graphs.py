# installed with default python
import time
from collections import deque

# need to be installed by user
import matplotlib.animation as animation
from matplotlib.backends import qt4_compat
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt4.QtGui import *
from PyQt4.QtCore import *

# included in github repo
import SensorSimulator   # for testing purposes only

# For testing when no real data coming in
TEST_DATA_ENABLED = True

class ScrollingGraph:

    ''' controls the buffer and updating of the scrolling
    sensor graphs
    needs to import deque
    '''

    def __init__(self, max_len, data_fn):
        # initializes buffer with max length, initializes data source
        self.ax = deque([0.0]*max_len)
        self.max_len = max_len
        self.data_fn = data_fn
        # data_fn is currently a function that produces random data


    def add_to_buffer(self, data):
        # adds value to buffer; if buffer is full, removes last value
        if TEST_DATA_ENABLED:
            if len(self.ax) < self.max_len:
                self.ax.appendleft(data)
            else:
                self.ax.pop()
                self.ax.appendleft(data)
        else:
            for val in data:
                if len(self.ax) < self.max_len:
                    self.ax.appendleft(val)
                else:
                    self.ax.pop()
                    self.ax.appendleft(val)

    def update(self, data):
        # gets new data from data function, adds it to the buffer
        # data is 4 element array of newest data, passed from main.py
        if TEST_DATA_ENABLED:
            data = self.data_fn()
            self.add_to_buffer(data)

            return self.ax
        else:
            self.add_to_buffer(data)


class MPLCanvas(FigureCanvas):

    '''
    canvas for mpl graph to be displayed in gui

    needs to import:
    Figure from matplotlib.figure,
    qt4_compat from matplotlib.backends,
    QtGui from PyQt4
    '''

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # creates figure, adds axes, sets qt size policy
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.axes.hold(False)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class DynamicGraphCanvas(MPLCanvas):

    '''
    extends MPLCanvas to dynamic canvas that will update
    automatically with timer
    needs to import:
    QtCore from PyQt4
    matplotlib
    '''


    def __init__(self, graph_x_data, dog, line_colour='b', **kwargs):
        # initializes mpl canvas with attributes update rate,
        # the ScrollingGraph object that will be providing the
        # data, line colour and the timer that will control the
        # updating of the graph
        MPLCanvas.__init__(self, **kwargs)
        self.update_rate = 100
        self.graph_x_data = graph_x_data
        self.line_colour = line_colour
        self.dict_of_graphs = dog
        timer = QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(self.update_rate)

    def compute_initial_figure(self):
        # initializes the figure, plots no data
        self.axes.plot([], [])

    def graph_change_handler(self, graph_of_sensor):
        # called when user changes the graph being displayed using
        # combo box, changes the ScrollingGraph object that will
        # be queried for data
        self.graph_x_data = self.dict_of_graphs[str(graph_of_sensor)]

    def update_figure(self):
        # called when timer runs out, calls update function of the
        # ScrollingGraph object being used as the data source,
        # redraws the graph
        # No longer used if data coming in, graphs should update automatically
        # when new data comes in
        if TEST_DATA_ENABLED:
            self.axes.plot(range(self.graph_x_data.max_len),\
                self.graph_x_data.update([]), self.line_colour)
            self.draw()
        else:
            self.axes.plot(range(self.graph_x_data.max_len),\
                self.graph_x_data.ax, self.line_colour)
            self.draw()
