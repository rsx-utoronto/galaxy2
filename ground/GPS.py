import serial
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.marble import *
import sys
import os
from math import *

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
		print "Angles"
		print (angle1, angle2, angle3)

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
		print "Point 1"
		print (p1LONG, p1LAT)

		p2LONG = px + l2x
		p2LAT = py + l2y
		p2 = Marble.GeoDataCoordinates(p2LONG, p2LAT, 0.0, Marble.GeoDataCoordinates.Degree)
		print "Point 2"
		print (p2LONG, p2LAT)
		
		p3LONG = px + l3x
		p3LAT = py + l3y
		p3 = Marble.GeoDataCoordinates(p3LONG, p3LAT, 0.0, Marble.GeoDataCoordinates.Degree)
		print "Point 3"
		print (p3LONG, p3LAT)

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
		# center the map on Kiev
		self.marble.centerOn(center);
		# set the zoom
		self.marble.setZoom(4000)

		self.marble.model().addGeoDataFile(inputfile)
	 
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

def main():
    	app = QApplication(sys.argv)
 	
	UTIAS = Marble.GeoDataCoordinates(-79.466083, 43.782247, 0, Marble.GeoDataCoordinates.Degree)

 	window = Window(UTIAS,'UTIASTest.osm','/dev/ttyUSB0','/dev/ttyUSB1')
    	window.startRover()
 
    	app.exec_()
 
main()
