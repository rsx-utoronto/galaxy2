# Test reading from the serial port
import serial
import time 

ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
ser.flush() 
c = 0

while(True): 
    byte = ser.read()
    if byte != "":
        print(ord(byte))
    else:
        print("EMPTY") 
    ser.write(chr(c))
    c = (c + 1) % 256
    #time.sleep(1) 
