from PyQt4.QtCore import *
import serial

import PacketSerial

class SensorGetter:

    def __init__(self, sensor_read_addresses, sensors, ser, pser):
        self.sensor_read_addresses = sensor_read_addresses
        self.sensors = sensors
        self.ser = ser
        self.pser = pser

        self.timer = QTimer(self)

        # signal to be emitted with data when sensor data is received, will
        # connect to an update function on the graphs, needs to be tested
        self.data_received = pyqtSignal(list)

    def start_sg(self):
        self.timer.setInterval(0)
        self.connect(self.timer, SIGNAL('timeout()'), self.main)
        self.timer.start()

    def end_sg(self):
        self.timer.stop()
    
    def main(self):
        if self.pser.available():
            data = self.pser.read() 
            if data is not None:
                try:
                    ind = self.sensor_read_addresses.index(data[0]) # which sensor block is this? 
                    self.sensors[ind*4:ind*4+4] = data[1:5]
                except ValueError:
                    pass # index not found

        # emit signal containing sensor data
        self.data_received.emit(self.sensors)
