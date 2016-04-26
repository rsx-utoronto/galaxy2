import time
from collections import deque

import matplotlib.animation as animation
from matplotlib.backends import qt4_compat
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import SensorSimulator

class scrolling_graph:

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


    def add_to_buffer(self, buf, val):
        # adds value to buffer; if buffer is full, removes last value
        if len(buf) < self.max_len:
            buf.appendleft(val)
        else:
            buf.pop()
            buf.appendleft(val)


    def update(self):
        # gets new data from data function, adds it to the buffer
        data = self.data_fn()
        self.add_to_buffer(self.ax, data)

        return self.ax


class mpl_canvas(FigureCanvas):

    ''' canvas for mpl graph to be displayed in gui

        needs to import:
        Figure from matplotlib.figure,
        qt4_compat from matplotlib.backends,
        QtGui from PyQt4 '''

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


class dynamic_graph_canvas(mpl_canvas):

    ''' extends mpl canvas to dynamic canvas that will update
        automatically with timer
        needs to import:
        QtCore from PyQt4
        matplotlib '''

    # possible sensors that the user can select from to graph,
    # dictionary for easy access by name
    gas_sensor = scrolling_graph(200, SensorSimulator.gas_sensor)
    moisture_sensor = scrolling_graph(200, SensorSimulator.moisture_sensor)
    graphs_of_sensors = {'Gas Sensor':gas_sensor,\
    'Moisture Sensor':moisture_sensor}

    def __init__(self, graph_x_data, line_colour='b', **kwargs):
        # initializes mpl canvas with attributes update rate,
        # the scrolling_graph object that will be providing the
        # data, line colour and the timer that will control the
        # updating of the graph
        mpl_canvas.__init__(self, **kwargs)
        self.update_rate = 100
        self.graph_x_data = graph_x_data
        self.line_colour = line_colour
        timer = QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(self.update_rate)

    def compute_initial_figure(self):
        # initializes the figure, plots no data
        self.axes.plot([], [])

    def graph_change_handler(self, graph_of_sensor):
        # called when user changes the graph being displayed using
        # combo box, changes the scrolling_graph object that will
        # be queried for data
        self.graph_x_data = dynamic_graph_canvas.graphs_of_sensors\
            [str(graph_of_sensor)]

    def update_figure(self):
        # called when timer runs out, calls update function of the
        # scrolling_graph object being used as the data source,
        # redraws the graph
        self.axes.plot(range(self.graph_x_data.max_len),\
            self.graph_x_data.update(), self.line_colour)
        self.draw()
