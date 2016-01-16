#serial for internal sensors
import serial

ser = serial.Serial("/dev/cu.usbmodem641", 9600, timeout = 0.01, writeTimeout = 0.01) #for mac
# change address to COM1 on windows or /dev/ttyUSB0 on linux. 
# The address is whatever is in the bottom right corner of the arduino windows
while(True):
    temp = ser.read()
    if temp != '':
        print(temp)
    # if you want a bit stream, use an array of ints 
 