import smbus
import time 

bus = smbus.SMBus(1)
SLAVE_ADD = 0x8
ctr = 0

while(True):
    bus.write_byte(SLAVE_ADD, ctr)
    ctr = (ctr + 1) % 256
    print(ctr) 
    time.sleep(0.1) 
