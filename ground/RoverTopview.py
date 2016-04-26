from PyQt4.QtCore import *
from PyQt4.QtGui import *

import SensorSimulator

class RoverTopview(QLabel):

    ''' A class that gives the topview of the six rover wheels, coloured
        according to temperature readings. '''

    def __init__(self):
        QLabel.__init__(self)
        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)       # how often the colours will update

    def paintEvent(self, event):
        colour1, colour2, colour3, colour4, colour5, colour6 = self.choose_colour()
        qp = QPainter()
        qp.begin(self)
        qp.setPen(Qt.black)
        qp.fillRect(0, 0, 50, 90, colour1)
        qp.fillRect(0, 175, 50, 90, colour2)
        qp.fillRect(0, 280, 50, 90, colour3)
        qp.fillRect(190, 0, 50, 90, colour4)
        qp.fillRect(190, 175, 50, 90, colour5)
        qp.fillRect(190, 280, 50, 90, colour6)
        qp.end()

    def choose_colour(self):

        ''' Chooses colours for the wheel pictures based on temperature readings.
            Currently gets random temperature readings from the sensor simulator
            file. '''

        temp1 = SensorSimulator.temp_sensor1()
        temp2 = SensorSimulator.temp_sensor2()
        temp3 = SensorSimulator.temp_sensor3()
        temp4 = SensorSimulator.temp_sensor4()
        temp5 = SensorSimulator.temp_sensor5()
        temp6 = SensorSimulator.temp_sensor6()

        colour1 = QColor(temp1*4, 0, 0)
        colour2 = QColor(temp2*4, 0, 0)
        colour3 = QColor(temp3*4, 0, 0)
        colour4 = QColor(temp4*4, 0, 0)
        colour5 = QColor(temp5*4, 0, 0)
        colour6 = QColor(temp6*4, 0, 0)

        return colour1, colour2, colour3, colour4, colour5, colour6
