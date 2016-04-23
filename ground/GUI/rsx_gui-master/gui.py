import sys
import os
from matplotlib.backends import qt4_compat
use_pyside = qt4_compat.QT_API == qt4_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from collections import OrderedDict

import graphs
import sensor_simulator

import random
import serial
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.marble import *
from math import *

import pygame 
import serial
import time 
from PacketSerial import *
import Joystick


class rover_topview(QtGui.QLabel):

    def __init__(self):
        QtGui.QLabel.__init__(self)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)

    def paintEvent(self, event):
        colour1, colour2, colour3, colour4, colour5, colour6 = self.choose_colour()
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(QtCore.Qt.black)
        qp.fillRect(0, 0, 50, 90, colour1)
        qp.fillRect(0, 175, 50, 90, colour2)
        qp.fillRect(0, 280, 50, 90, colour3)
        qp.fillRect(190, 0, 50, 90, colour4)
        qp.fillRect(190, 175, 50, 90, colour5)
        qp.fillRect(190, 280, 50, 90, colour6)
        qp.end()

    def choose_colour(self):
        temp1 = sensor_simulator.temp_sensor1()
        temp2 = sensor_simulator.temp_sensor2()
        temp3 = sensor_simulator.temp_sensor3()
        temp4 = sensor_simulator.temp_sensor4()
        temp5 = sensor_simulator.temp_sensor5()
        temp6 = sensor_simulator.temp_sensor6()

        colour1 = QtGui.QColor(temp1*4, 0, 0)
        colour2 = QtGui.QColor(temp2*4, 0, 0)
        colour3 = QtGui.QColor(temp3*4, 0, 0)
        colour4 = QtGui.QColor(temp4*4, 0, 0)
        colour5 = QtGui.QColor(temp5*4, 0, 0)
        colour6 = QtGui.QColor(temp6*4, 0, 0)

        return colour1, colour2, colour3, colour4, colour5, colour6

class GPSWorker(QObject):
	def __init__(self,serialPort):
		QObject.__init__(self)
		# initialize the worker's data
		try:
			self.ser = serial.Serial(serialPort,4800,timeout=1)
		except:
			print "The GPS is not connected to the current serial port"
		self.timer = QTimer(self)
		self.alpha = 0.0
		self.cnt = 0
	
	def convertDD(self,value):
		#GPS returns Degrees Decimal Minutes, this converts in into purely Degrees (Marble converts it into DMS automatically)
		value = value/100
		deg = int(value)
		minutes = (value - deg)*100
		return deg + minutes/60

	def startWork(self):
		self.timer.setInterval(0)
		#change self.pseudoiterate to self.iterate when GPS is connected
		self.connect(self.timer, SIGNAL('timeout()'), self.pseudoiterate) #pseudoiterate is used as a test when the GPS is not connected
		self.timer.start()

	def iterate(self):
		# update the loaction of the current worker
		while True:
			line = self.ser.readline()
			if not line.strip():
				print "GPS is not connected"
			if "GPGGA" in line:
				line = line.split(',')
				try:
					latitude = float(line[2])
					longitude = float(line[4])
				except:
					print "GPS is not receiving a satellite signal"
					print line
					return

				latitude = self.convertDD(latitude)
				longitude = self.convertDD(longitude)

				#Converting N/S into +/- coordinates
				if line[3] == 'S':
					latitude = latitude * -1
				else:
					latitude = latitude

				#convering E/W into +/- coordinates
				if line[5] == 'W':
					longitude = longitude * -1
				else:
					longitude = longitude
	
				break
		coord = Marble.GeoDataCoordinates(longitude, latitude, 0.0, Marble.GeoDataCoordinates.Degree)
		self.emit(SIGNAL("coordinatesChanged(PyQt_PyObject)"), coord)

	#used as testing only, moves the "rover" straight upwards
	def pseudoiterate(self):
		#Used for testing purposes when the GPS is not available
		#Centers the test at UTIAS
		initialLat = 4346.9345
		initialLong = -7927.9650
	
		#Moves the rover continuously upwards
		latitude = initialLat + self.cnt * 0
		longitude = initialLong

		latitude = self.convertDD(latitude)
		longitude = self.convertDD(longitude)

		coord = Marble.GeoDataCoordinates(longitude, latitude, 0.0, Marble.GeoDataCoordinates.Degree)
		self.cnt = self.cnt + 1
		self.emit(SIGNAL("coordinatesChanged(PyQt_PyObject)"), coord)
	 
	def finishWork(self):
		self.timer.stop()

class CompassWorker(QObject):
	#THIS STILL NEEDS AN ITERATE FUNCTION THAT CONNECTS TO A REAL COMPASS
	def __init__(self,serialPort,centerOn):
		QObject.__init__(self)
		self.timer = QTimer(self)
		self.alpha = 0.0
		self.cnt = 0
		self.position = centerOn
		self.cnt = 0
	
	def startWork(self):
		self.timer.setInterval(0)
		self.connect(self.timer, SIGNAL('timeout()'), self.pseudoiterate) #same thing here, except there is no real iterate yet cause of no compass data
		self.timer.start()

	def calculatePoints(self,heading):
		#May be shorter to package some of this stuff into functions, but it isn't really necessary
		#Size of the heading triangle
		scale = 0.00005

		#Compute three points on the heading triangle
		angle1 = heading
		angle2 = 3.14 + heading - 0.64
		angle3 = 3.14 + heading + 0.64
#		print "Angles"
#		print (angle1, angle2, angle3)

		#Compute the offset of the three points from the current location point

		l1x = scale * cos(angle1)
		l1y = scale * sin(angle1)

		l2x = scale * cos(angle2)
		l2y = scale * sin(angle2)

		l3x = scale * cos(angle3)
		l3y = scale * sin(angle3)

		#Position 
		px = self.position.longitude(Marble.GeoDataCoordinates.Degree)
		py = self.position.latitude(Marble.GeoDataCoordinates.Degree)

		p1LONG = px + l1x
		p1LAT = py + l1y
		p1 = Marble.GeoDataCoordinates(p1LONG, p1LAT, 0.0, Marble.GeoDataCoordinates.Degree)
#		print "Point 1"
#		print (p1LONG, p1LAT)

		p2LONG = px + l2x
		p2LAT = py + l2y
		p2 = Marble.GeoDataCoordinates(p2LONG, p2LAT, 0.0, Marble.GeoDataCoordinates.Degree)
#		print "Point 2"
#		print (p2LONG, p2LAT)
		
		p3LONG = px + l3x
		p3LAT = py + l3y
		p3 = Marble.GeoDataCoordinates(p3LONG, p3LAT, 0.0, Marble.GeoDataCoordinates.Degree)
#		print "Point 3"
#		print (p3LONG, p3LAT)

		return (p1,p2,p3)
			
	#currently just spins the "rover" in circles
	def pseudoiterate(self):
		initialCompass = 0
		compassReading = initialCompass + self.cnt * 0.1
		
		heading = self.calculatePoints(compassReading)
		self.cnt = self.cnt + 1
		self.emit(SIGNAL("headingChanged(PyQt_PyObject)"), heading)		

	def finishWork(self):
		self.timer.stop()
	
#GUI widget
class Window(QWidget):
	def __init__(self,center,inputfile,GpsSerialPort,CompassSerialPort):
		QWidget.__init__(self)
		self.GpsSerialPort = GpsSerialPort
		self.CompassSerialPort = CompassSerialPort
		self.startLocation = center
	 
		# create the marble widget
		self.marble = Marble.MarbleWidget()
	 
		# resize the widget and add a window title
		self.resize(1000, 800)
		self.setWindowTitle("RSX GPS Tracking")
	 
		layout = QVBoxLayout(self)
		layout.addWidget(self.marble)
		self.setLayout(layout)
	 
		# load the OpenStreetMap map
		self.marble.setMapThemeId("earth/google-maps-satellite/google-maps-satellite.dgml")
		self.marble.setProjection(Marble.Mercator)
		# center the map on UTIAS
		self.marble.centerOn(center);
		# set the zoom
		self.marble.setZoom(4000)
	 
		# create the placemarks and their containing document
		self.H1 = Marble.GeoDataPlacemark()
		self.H2 = Marble.GeoDataPlacemark()
		self.H3 = Marble.GeoDataPlacemark()
#		self.triangle = Marble.GeoDataPlacemark()
		self.rover = Marble.GeoDataPlacemark("Rover")
		
		self.document = Marble.GeoDataDocument()
	 
		self.document.append(self.rover)
#		self.document.append(self.triangle)
		self.document.append(self.H1)
		self.document.append(self.H2)
		self.document.append(self.H3)
	 
		# add the placemark document to the map
		self.marble.model().treeModel().addDocument(self.document);
	 
		# add the widget to the KMainWindow
		self.show()
	
	def startRover(self):
		# create the thread for the GPS coordinates
		self.gpsthread = QThread()
		self.gpsWorker = GPSWorker(self.GpsSerialPort)
		self.gpsWorker.moveToThread(self.gpsthread)

		# create the thread for the compass coordinates
		self.compassthread = QThread()
		self.compassWorker = CompassWorker(self.CompassSerialPort,self.startLocation)
		self.compassWorker.moveToThread(self.compassthread)
	 
		self.connect(self.gpsWorker, SIGNAL("coordinatesChanged(PyQt_PyObject)"),self.setRoverCoordinates, Qt.BlockingQueuedConnection)
		self.connect(self.compassWorker, SIGNAL("headingChanged(PyQt_PyObject)"),self.setRoverHeading, Qt.BlockingQueuedConnection)
	 
		# when both the threads start, begin running the workers
		self.connect(self.gpsthread, SIGNAL("started()"), self.gpsWorker.startWork)
		self.connect(self.gpsthread, SIGNAL("finished()"), self.gpsWorker.finishWork)

		self.connect(self.compassthread, SIGNAL("started()"), self.compassWorker.startWork)
		self.connect(self.compassthread, SIGNAL("finished()"), self.compassWorker.finishWork)

		# start the threads
		self.gpsthread.start()
		self.compassthread.start()
 
	def setRoverCoordinates(self, coord):
		self.rover.setCoordinate(coord)
		self.marble.model().treeModel().updateFeature(self.rover)
		self.compassWorker.position = coord

	def setRoverHeading(self, points):
		self.H1.setCoordinate(points[0])
		self.marble.model().treeModel().updateFeature(self.H1)
		self.H2.setCoordinate(points[1])
		self.marble.model().treeModel().updateFeature(self.H2)
		self.H3.setCoordinate(points[2])
		self.marble.model().treeModel().updateFeature(self.H3)


class application_window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")
        self.resize(1000, 1000)

        # --- Menu --- #
        self.file_menu = QtGui.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        # --- Widgets --- #
        self.tabs = QtGui.QTabWidget()
        self.graph_widget = QtGui.QWidget()
        self.map_widget = QtGui.QWidget()
        self.topview_widget = QtGui.QWidget()

        # Combo box for selecting which graphs to view
        self.graph_chooser_top = QtGui.QComboBox(self.graph_widget)
        self.graph_chooser_top.addItems(['Gas Sensor', 'Moisture Sensor'])
        self.graph_chooser_bottom = QtGui.QComboBox(self.graph_widget)
        self.graph_chooser_bottom.addItems(['Gas Sensor', 'Moisture Sensor'])

        # Dynamic canvases to hold graphs
        dc1 = graphs.dynamic_graph_canvas(graphs.dynamic_graph_canvas.\
            gas_sensor, parent=self.graph_widget, width=5, height=4, dpi=100)
        dc2 = graphs.dynamic_graph_canvas(graphs.dynamic_graph_canvas.\
            moisture_sensor, parent=self.graph_widget, width=5, height=4, dpi=100)

        # Make map widget
        UTIAS = Marble.GeoDataCoordinates(-79.466083, 43.782247, 0, Marble.GeoDataCoordinates.Degree)
        gps_map = Window(UTIAS,'UTIASTest.osm','/dev/ttyUSB0','/dev/ttyUSB1')
        
        # Start joystick
        self.joystick_thread = QThread()
        self.j = Joystick.Joystick()
        self.j.moveToThread(self.joystick_thread)

        self.connect(self.joystick_thread, SIGNAL("started()"), self.j.start_joystick)
        self.connect(self.joystick_thread, SIGNAL("finished()"), self.j.end_joystick)

        self.joystick_thread.start()

        # Coloured wheels widget
        rov = rover_topview()

        # Box layout for graph_widget, holds 2 graph canvases and combo box
        l = QtGui.QHBoxLayout()
        v1 = QtGui.QVBoxLayout()
        v2 = QtGui.QVBoxLayout()
        v1.addWidget(dc1)
        v1.addWidget(self.graph_chooser_top)
        v2.addWidget(dc2)
        v2.addWidget(self.graph_chooser_bottom)
        l.addLayout(v1)
        l.addLayout(v2)
        self.graph_widget.setLayout(l)

        # Horizontal box layout for map_widget, holds label with map image
        l2 = QtGui.QHBoxLayout()
        l2.addWidget(gps_map)
        self.map_widget.setLayout(l2)

        # Layout for topview_widget
        l3 = QtGui.QHBoxLayout()
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

    qApp = QtGui.QApplication(sys.argv)
    qApp.setWindowIcon(QtGui.QIcon('icon.png'))

    aw = application_window()
    sys.exit(qApp.exec_())
    #qApp.exec_()
