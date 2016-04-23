import serial 
import time 
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
# pser = PacketSerial(ser)
ctr = 0

while(True):
    ctr += 1
    print(ser.read())
    ser.write(chr(ctr))
    #pser.write(('d', 'e', 'f', chr(ctr)))
    time.sleep(0.01)
