# Main running on ground station. No GPS or GUI for now
import pygame 
import serial
import time 
from PacketSerial import *
import sys, os

pygame.init()
j = pygame.joystick.Joystick(0)
j.init() 
pygame.joystick.init()

ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
pser = PacketSerial(ser)
starttime = time.time() 

# Define some constants
ARM_ADDRESS = chr(0x10)  # since pyserial likes to get them as strings. 
SENSOR_ADDRESS = chr(0x11)
DRIVE_ADDRESS = chr(0x12)

joystick_controls_arm = False

while(True):
    for event in pygame.event.get(): # User did something
        pass   # ignore events.
    
    if (joystick_controls_arm): # send joystick commands to the arm 
        if(abs(j.get_axis(1)) < 0.1): 
            pser.write((ARM_ADDRESS, '0', '\x00', '\x00')) # don't let drift affect the arm
        elif(j.get_axis(1) > 0):
            pser.write((ARM_ADDRESS, '2', '\x00', '\x00'))
        else:
            pser.write((ARM_ADDRESS, '1', '\x00', '\x00')) 
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
        pser.write((DRIVE_ADDRESS, chr(left_right), chr(forward_backward), '\x07'))
        
    # Switch between arm and drive system 
    if j.get_button(9):
        joystick_controls_arm = not joystick_controls_arm
        print("Switched joystick control of arm/ drive")
        # TODO: Stop all motion when switching between systems

    data = pser.read()
    data2 = pser.read()
    print("Sensor data: ", data, data2)

    #time.sleep(0.1)
    if time.time() - starttime > 5:
        ser.flushInput() 
        ser.flushOutput()
        starttime = time.time()
