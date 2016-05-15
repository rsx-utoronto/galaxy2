import sys
import os
import time 

import pygame 
import serial
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PacketSerial import *

class Joystick(QObject):

    ''' all of chris' joystick code '''

    def __init__(self, arm_address, drive_address, ser, pser):
        QObject.__init__(self)
        pygame.init()
        self.j = pygame.joystick.Joystick(0)
        self.j.init()
        pygame.joystick.init()

        self.arm_address = arm_address
        self.drive_address = drive_address
        self.ser = ser
        self.pser = pser
        self.starttime = time.time()
        self.timer = QTimer(self)

        self.joystick_controls_arm = False
        self.joint_to_control = 1

        self.system_to_control_changed = pyqtSignal(bool)
        self.joint_to_control_changed = pyqtSignal(int)

    def start_joystick(self):
		self.timer.setInterval(0)
		self.connect(self.timer, SIGNAL('timeout()'), self.main)
		self.timer.start()

    def end_joystick(self):
        self.timer.stop()

    def main(self):
        for event in pygame.event.get(): # User did something
            pass   # ignore events.
        
        if (self.joystick_controls_arm): # send joystick commands to the arm 
            '''if(abs(self.j.get_axis(1)) < 0.1): 
                self.pser.write((self.arm_address, '0', '\x00', '\x00')) # don't let drift affect the arm
            elif(self.j.get_axis(1) > 0):
                self.pser.write((self.arm_address, '2', '\x00', '\x00'))
            else:
                self.pser.write((self.arm_address, '1', '\x00', '\x00')) '''
            # decide what to do with arm on arduino side
            x = int(self.j.get_axis(1))
            y = int(self.j.get_axis(2))
            self.pser.write((self.arm_address, chr(self.joint_to_control), chr(x), chr(y)))
        else:  # joystick controls drive system
            '''vertical_axis = self.j.get_axis(1)#vertical_axis input
            horizontal_axis = self.j.get_axis(0)# horizontal_axis input
            lever = -(self.j.get_axis(2)-1)/2 #the shiftable joystick in the bottom "+" and "-" to control the speed, scaled to the desired high to low position

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
                left_right=93 #rest values- no motion '''
            forward_backward = int(self.j.get_axis(1) * 100 + 100)
            left_right = int(self.j.get_axis(2) * 100 + 100)
            self.pser.write((self.drive_address, chr(left_right), chr(forward_backward), '\x07'))
            self.pser.write((self.drive_address, chr(left_right), chr(forward_backward), '\x07'))
            
        # Switch between arm and drive system 
        if self.j.get_button(9):
            self.joystick_controls_arm = not self.joystick_controls_arm
            self.system_to_control_changed.emit(self.joystick_controls_arm)
            print("Switched joystick control of arm/ drive")
            # TODO: Stop all motion when switching between systems

        # switch between joints when controlling arm
        if self.joystick_controls_arm == True and self.j.get_button(8): # button 8 chosen randomly, feel free to change
            if self.joint_to_control < 3:        # currently assuming 3 joints, TODO update when number of joints known
                self.joint_to_control += 1
            elif self.joint_to_control == 3:
                self.joint_to_control = 1
            self.joint_to_control_changed.emit(self.joint_to_control)

        #data = self.pser.read()
        #data2 = self.pser.read()
        #print("Sensor data: ", data, data2)

        #time.sleep(0.1)
        if time.time() - self.starttime > 5:
            self.ser.flushInput() 
            self.ser.flushOutput()
            self.starttime = time.time()

    def joystick_controls_arm_button(self, arg):
        
        self.joystick_controls_arm = arg
        print self.joystick_controls_arm  # testing purposes only

    def joint_to_control_button(self, joint):

        self.joint_to_control = joint
