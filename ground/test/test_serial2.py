# Test reading and writing simultaneously from the serial port
import serial
import time

ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
# pser = PacketSerial(ser)
ctr = 0

while(True): 
    ctr += 1
    ser.write(chr(ctr))
    print(ser.read())
    time.sleep(0.01)
