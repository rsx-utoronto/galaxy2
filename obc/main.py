import pygame
import smbus
import time 
import serial 
from PacketSerial import *

# initialize things 
bus = smbus.SMBus(1)
ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)
pser = PacketSerial(ser)

# define constants
ARM_ADDRESS = 0x10
SENSOR_ADDRESS = 0x11
DRIVE_ADDRESS = 0x12
SENSOR_2_ADDRESS = 0x80 # for when we send data over serial 

# define places to hold the data
drive = [-1, -1] # Holds most recent data sent to the motors. 
sensors = [0 for i in range(6)]  # moisture, gas1, gas2, gas3, voltage
joystick_controls_arm = False
i2cwritetime = flushtime = time.time() 

def write(address, data):
    '''
    Write a byte to the i2c connection
    Arguments:
        address (int): i2c address of the receiving device
        data (char): data to be sent
    '''
    bus.write_byte(address, ord(data))

def read(address):
    '''
    Read a byte from the i2c connection
    Argument:
        address (int): i2c address of the receiving device
    '''    
    return bus.read_byte(address)
    
def read_block(address):
    ''' 
    Read a whatever block of data was sent across the i2c connection.
    Will always return a 32-byte array with 255 in the unused positions. 
    Argument: 
        address (int): i2c address of the receiving device 
    '''
    return bus.read_i2c_block_data(address, 0)

def write_block(address, data):
    '''
    Write a block of data across the i2c connection
    ''' 
    if len(data) == 0:
        raise IndexError("You cannot write 0 bytes across the i2c connection")
    elif len(data) == 1:
            bus.write_byte(address,data[0])
    else:
        bus.write_i2c_block_data(address, data[0], data[1:])

def to_strs(*lis):
    return list(chr(i) for i in lis)

while(True):
    data = pser.read() 
    # print("Received data: ", data)
    
    if data is None:
        # Do nothing. no data received. 
        pass
    else:    
        if ord(data[0]) == ARM_ADDRESS: #these might not be separate cases, I might just use write_block for everything
            write(ARM_ADDRESS, data[1])
        elif ord(data[0]) == DRIVE_ADDRESS:
            drive = [ord(i) for i in data[1:3]]
    # get sensor data
    sensors = [read(SENSOR_ADDRESS) for i in range(5)] # is this correct or do I need to use readblock? 
    print("Read sensors", sensors)
    #pser.write(to_strs(SENSOR_ADDRESS, sensors[0], sensors[1], sensors[2]))
    #pser.write(to_strs(SENSOR_2_ADDRESS, sensors[3], sensors[4], sensors[5]))
    #time.sleep(0.1) # poll at a limited rate. 

    if time.time() - i2cwritetime > 0.3:
        
        if -1 not in drive: 
            write_block(DRIVE_ADDRESS, drive)
        i2cwritetime = time.time()
        try:
            print("Wrote to drive", drive)
            write_block(DRIVE_ADDRESS, drive) # should actually restart script
        except IOError:
            print("IO Error. Ignoring") 
    if time.time() - flushtime > 1:
        ser.flushInput() # flush the buffer at limited intervals
        ser.flushOutput() # flush the buffer at limited intervals
        flushtime = time.time() 
        print("=====================FLUSHED=====================================================")
        '''if drive != [-1, -1]:
            try:
                print("Wrote to drive", drive)
                write_block(DRIVE_ADDRESS, drive)
            except IOError:
                print("IO Error. Ignoring") 
            drive = [-1, -1] '''
