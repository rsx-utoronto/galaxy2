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
import SensorSimulator
import RoverTopview


# define constants here
ARM_ADDRESS = chr(0x10)  # since pyserial likes to get them as strings. 
SENSOR_ADDRESS = chr(0x11)  # doesn't seem to be used anywhere, do we still need this?
DRIVE_ADDRESS = chr(0x12)
SENSOR_READ_ADDRESSES = [chr(0x80), chr(0x81), chr(0x82), chr(0x83), chr(0x84), chr(0x85), ]
SENSORS = [0 for i in range(16)] 

# since these are (I think) common throughout
try:
    ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
    pser = PacketSerial(self.ser)
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

        # Combo box for selecting which graphs to view
        self.graph_chooser_top = QComboBox(self.graph_widget)
        self.graph_chooser_top.addItems(['Gas Sensor', 'Moisture Sensor'])
        self.graph_chooser_bottom = QComboBox(self.graph_widget)
        self.graph_chooser_bottom.addItems(['Gas Sensor', 'Moisture Sensor'])

        # Dynamic canvases to hold graphs
        dc1 = Graphs.dynamic_graph_canvas(Graphs.dynamic_graph_canvas.\
            gas_sensor, parent=self.graph_widget, width=5, height=4, dpi=100)
        dc2 = Graphs.dynamic_graph_canvas(Graphs.dynamic_graph_canvas.\
            moisture_sensor, parent=self.graph_widget, width=5, height=4, dpi=100)

        # Make map widget
        if GPSGui.marble_imported:                    # see import statement at top for reason
            UTIAS = Marble.GeoDataCoordinates(-79.466083, 43.782247, 0, Marble.GeoDataCoordinates.Degree)
            gps_map = GPSGui.GPSMapWidget(UTIAS,'UTIASTest.osm','/dev/ttyUSB0','/dev/ttyUSB1')
        
        # Start joystick
        try:                      # so that it can still run without joystick connected
            self.joystick_thread = QThread()
            self.j = Joystick.Joystick(ARM_ADDRESS, DRIVE_ADDRESS, ser, pser)
            self.j.moveToThread(self.joystick_thread)

            self.connect(self.joystick_thread, SIGNAL("started()"), self.j.start_joystick)
            self.connect(self.joystick_thread, SIGNAL("finished()"), self.j.end_joystick)

            self.joystick_thread.start()
        except:
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

        # Box layout for graph_widget, holds 2 graph canvases and combo box
        l = QHBoxLayout()
        v1 = QVBoxLayout()
        v2 = QVBoxLayout()
        v1.addWidget(dc1)
        v1.addWidget(self.graph_chooser_top)
        v2.addWidget(dc2)
        v2.addWidget(self.graph_chooser_bottom)
        l.addLayout(v1)
        l.addLayout(v2)
        self.graph_widget.setLayout(l)

        # Horizontal box layout for map_widget, holds label with map image
        l2 = QHBoxLayout()
        if GPSGui.marble_imported:    # see import for reason
            l2.addWidget(gps_map)
        self.map_widget.setLayout(l2)

        # Layout for topview_widget
        l3 = QHBoxLayout()
        l3.addWidget(rov)
        self.topview_widget.setLayout(l3)

        # Combo box event
        self.graph_chooser_top.activated[str].connect(dc1.graph_change_handler)
        self.graph_chooser_bottom.activated[str].connect(dc2.graph_change_handler)

        # Create tabs
        self.tabs.addTab(self.graph_widget, 'Graphs')
        self.tabs.addTab(self.map_widget, 'Map')
        self.tabs.addTab(self.topview_widget, 'Top View')

        self.tabs.setWindowTitle('RSX Rover Control')
        self.tabs.show()

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
