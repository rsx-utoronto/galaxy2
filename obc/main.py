import pygame
import smbus
import time 

# initialize things 
pygame.init()
j = pygame.joystick.Joystick(0)
j.init() 
pygame.joystick.init()
bus = smbus.SMBus(1)

# define constants
ARM_ADDRESS = 0x10
SENSOR_ADDRESS = 0x11

# define places to hold the data
sensors = [0 for i in range(5)]  # moisture, gas1, gas2, gas3, voltage

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
    
while(True):
    for event in pygame.event.get(): # User did something
        pass   # ignore events.

    # send joystick commands to the arm 
    if(j.get_button(1) == 1):
        write(ARM_ADDRESS, '2')
    elif(j.get_button(0) == 1):
        write(ARM_ADDRESS, '1') 

    # get sensor data
    sensors = [read(SENSOR_ADDRESS) for i in range(5)] 
    print(sensors) 
    time.sleep(0.25) # poll every 0.25 seconds    
