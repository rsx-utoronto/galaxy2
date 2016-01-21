#Requires Marble w/ Python bindings

import serial
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.marble import *
import sys
import os

class GPSWorker(QObject):
	def __init__(self,serialPort):
		QObject.__init__(self)
		# initialize the worker's data
		try:
			self.ser = serial.Serial(serialPort,4800,timeout=1)
		except:
			print "The GPS is not connected to the current serial port"
			#quit() #NOTE THE PROGRAM QUIT HERE -- this may or may not be desireable
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
		self.connect(self.timer, SIGNAL('timeout()'), self.pseudoiterate)
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
		print (longitude, latitude)
		self.emit(SIGNAL("coordinatesChanged(PyQt_PyObject)"), coord)

	def pseudoiterate(self):
		initialLat = 4346.9345
		initialLong = -7927.9650
	
		latitude = initialLat + self.cnt * 0.001
		longitude = initialLong

		latitude = self.convertDD(latitude)
		longitude = self.convertDD(longitude)

		coord = Marble.GeoDataCoordinates(longitude, latitude, 0.0, Marble.GeoDataCoordinates.Degree)
		print (longitude, latitude)
		self.cnt = self.cnt + 1
		self.emit(SIGNAL("coordinatesChanged(PyQt_PyObject)"), coord)
	 
	def finishWork(self):
		self.timer.stop()

class Window(QWidget):
	def __init__(self,center,inputfile,serialPort):
		QWidget.__init__(self)
		self.serialPort = serialPort
	 
		# create the marble widget
		self.marble = Marble.MarbleWidget()
	 
		# resize the widget and add a window title
		self.resize(1000, 800)
		self.setWindowTitle("RSX GPS Tracking")
	 
		layout = QVBoxLayout(self)
		layout.addWidget(self.marble)
		self.setLayout(layout)
	 
		# load the OpenStreetMap map
		self.marble.setMapThemeId("earth/openstreetmap/openstreetmap.dgml")
		self.marble.setProjection(Marble.Mercator)
		# center the map on Kiev
		self.marble.centerOn(center);
		# set the zoom
		self.marble.setZoom(3000)

		self.marble.model().addGeoDataFile(inputfile)
	 
		# create the placemarks and their containing document
		self.rover = Marble.GeoDataPlacemark("Rover")
	 
		self.document = Marble.GeoDataDocument()
	 
		self.document.append(self.rover)
	 
		# add the placemark document to the map
		self.marble.model().treeModel().addDocument(self.document);
	 
		# add the widget to the KMainWindow
		self.show()
	
	def startRover(self):
		# create the thread for the first car
		self.gpsthread = QThread()
		self.gpsWorker = GPSWorker(self.serialPort)
		self.gpsWorker.moveToThread(self.gpsthread)
	 
		self.connect(self.gpsWorker, SIGNAL("coordinatesChanged(PyQt_PyObject)"),
		        self.setRoverCoordinates, Qt.BlockingQueuedConnection)
	 
		# when both the threads start, begin running the workers
		self.connect(self.gpsthread, SIGNAL("started()"), self.gpsWorker.startWork)
		self.connect(self.gpsthread, SIGNAL("finished()"), self.gpsWorker.finishWork)

		# start the threads
		self.gpsthread.start()
 
	def setRoverCoordinates(self, coord):
		self.rover.setCoordinate(coord)
		self.marble.model().treeModel().updateFeature(self.rover)

def main():
    	app = QApplication(sys.argv)
 	
	UTIAS = Marble.GeoDataCoordinates(-79.466083, 43.782247, 0, Marble.GeoDataCoordinates.Degree)

 	window = Window(UTIAS,'UTIASTest.osm','/dev/ttyUSB0')
    	window.startRover()
 
    	app.exec_()
 
main()
