import socket, threading
from serial import *

##########RPi SERVER##########

HOST = '192.168.1.107' #RPi IP address
PORT = 51234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(4)
clients = [] #list of clients connected
lock = threading.Lock()

serPort = raw_input("Enter Arduino serial port number")
ser = Serial("/dev/ttyUSB" + serPort, 9600, timeout = 0.01, writeTimeout = 0.01)

class chatServer(threading.Thread):
    def __init__(self, (socket,address)):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address= address

    def run(self):
        lock.acquire()
        clients.append(self)
        lock.release()
        print '%s:%s connected.' % self.address
        while True:
            data = self.socket.recv(1024)
            if not data:
                break
            for c in clients:
                #c.socket.send(data)
		print data
		ser.write(str(data) + "\n")
        self.socket.close()
        print '%s:%s disconnected.' % self.address
        lock.acquire()
        clients.remove(self)
        lock.release()z

while True: # wait for socket to connect
    # send socket to chatserver and start monitoring
    chatServer(s.accept()).start()

https://github.com/rsx-utoronto/galaxy.git
