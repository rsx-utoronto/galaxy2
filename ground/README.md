
## *Ground Station*


#### *Included Files:*

###### *main.py*

Reads and sends input/output between the ground station and the rover. Starts/ends the communication system & GUI. 

Joystick.py dependencies:
------------------------------

- pygame (sudo apt-get install python-pygame, for some reason pip didn't work for me)
- pyserial (import as serial)
- PacketSerial (available in repo)
- PyQt4


gui.py dependencies:
--------------------------

- matplotlib
- PyQt4
- pyserial (import as serial)
- PyKDE4.marble
- pygame
- Joystick (available in repo)
- graphs (available in repo)
- sensor_simulator (module in repo, only needed for testing)
- PacketSerial (avaibable in repo)
- SensorGetter (available in repo)
