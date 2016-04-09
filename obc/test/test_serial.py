import serial, time
ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)
ser.flush() 
c = 0

while(True):
    ser.write(chr(c))
    c = (c - 1) % 256
    byte = ser.read()
    if byte != "":
        print(ord(byte))
    if c % 16 == 0:
        print("running") 
    #time.sleep(1)
