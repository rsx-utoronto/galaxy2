#to run, 'sudo python' then 'import gamepad' (this file), then 'gamepad.test()'
#to install pygame: apt-get install python-pygame

##########RPi CLIENT##########

import pygame, time, serial, math, socket, telnetlib

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()

tn = telnetlib.Telnet("192.168.1.150","51235") #RPi IP address
#tn = telnetlib.Telnet("100.64.249.58", "51234") #RPi IP address on UOFT

output_delay = 0.25

def get():
    out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    it = 0
    pygame.event.pump()
    
    for i in range(0, j.get_numaxes()):
        out[it] = round(j.get_axis(i), 2)
        it+=1
        
    #Read input from buttons
    for i in range(0, j.get_numbuttons()):
        out[it] = j.get_button(i)
        it+=1
    #return out

    for i in range(0, j.get_numhats()):
        out[it] = j.get_hat(i)
        it+=1
    return out

def test():
    while True:
        time.sleep(float(output_delay))
        joystick_info = get()
        tn.write(str(joystick_info).replace(" ","").replace("[","").replace("]","").replace("(","").replace(")",""))
        print str(joystick_info)

if __name__ == '__main__':
    test()
