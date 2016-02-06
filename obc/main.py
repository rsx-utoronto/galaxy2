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
DRIVE_ADDRESS = 0x12

# define places to hold the data
sensors = [0 for i in range(5)]  # moisture, gas1, gas2, gas3, voltage
joystick_controls_arm = False 

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
            bus.write(address, chr(data[0]))
    else:
	    bus.write_i2c_block_data(address, data[0], data[1:]) 

while(True):
    for event in pygame.event.get(): # User did something
        pass   # ignore events.

    # send joystick commands to the arm 
    if (joystick_controls_arm):
        if(abs(j.get_axis(1)) < 0.1):
            write(ARM_ADDRESS, '0') # don't let drift affect the arm
        elif(j.get_axis(1) > 0):
            write(ARM_ADDRESS, '2')
        else:
            write(ARM_ADDRESS, '1')
    else:  # joystick controls drive system
        vertical_axis=j.get_axis(1)#vertical_axis input
        horizontal_axis=j.get_axis(0)# horizontal_axis input
        lever=-(j.get_axis(2)-1)/2 #the shiftable joystick in the bottom "+" and "-" to control the speed, scaled to the desired high to low position
        
        if(vertical_axis*100<0):#when the vertical axis is pushed up
            forward_backward=93+vertical_axis*63*lever
            forward_backward=int(forward_backward)
        elif(vertical_axis*100>0):#when the vertical axis is pushed down
            forward_backward=93+vertical_axis*57*lever
            forward_backward=int(forward_backward)
           
        if(horizontal_axis*100<0):#when pushed left
            left_right=93+horizontal_axis*63*lever
            left_right=int(left_right)        
        elif(horizontal_axis*100>0):#when pushed right
            left_right=93+horizontal_axis*67*lever
            left_right=int(left_right)
           
        if(vertical_axis==0):
            forward_backward=93 #rest values- no motion
        if(horizontal_axis==0):
            left_right=93 #rest values- no motion

        write_block(DRIVE_ADDRESS, [left_right, forward_backward])
        
    # Switch between arm and drive system 
    if j.get_button(9):
        joystick_controls_arm = not joystick_controls_arm
        print("Switched joystick control of arm/ drive")
        # TODO: Stop all motion when switching between systems

    # get sensor data
    sensors = [read(SENSOR_ADDRESS) for i in range(5)] 
    print(sensors) 
    time.sleep(0.25) # poll every 0.25 seconds    
