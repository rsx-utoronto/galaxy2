class SensorGetter:

    def __init__(self, sensor_read_addresses, sensors, ser, pser):
        self.sensor_read_addresses = sensor_read_addresses
        self.sensors = sensors
        self.ser = ser
        self.pser = pser

        self.timer = QTimer(self)

    def start_sg(self):
        self.timer.setInterval(0)
        self.connect(self.timer, SIGNAL('timeout()'), self.main)
        self.timer.start()

    def end_sg(self):
        self.timer.stop()
    
    def main(self):
        while pser.available():
            data = pser.read() 
            if data is None:
                break
            try:
                ind = SENSOR_READ_ADDRESSES.index(data[0]) # which sensor block is this? 
                sensors[ind*4:ind*4+4] = data[1:5]
            except ValueError:
                pass # index not found
        print(sensors)
