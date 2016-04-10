import serial
from collections import deque
import hashlib

class PacketSerial():
	""" 
	Really hack class to write 4 serial packets at once.
	Note that the packets are not checked for orer. 
	Read and write both take 4 bits at once
	"""
	def __init__(self, serial_connection):	
		self.ser = serial_connection
		self.d = deque(["a", "a", "a", "a", "a"])
		self.counter = 0

	def read(self):
		"returns byte[4] or None"

		for i in range(6):
			byte = self.ser.read()	
			if byte is None or byte == "":
			    return None
			# check whether it's a checksum packet
			checksum = hashlib.md5("".join(self.d)).digest()[0]
			'''checksum = 0
			for i in self.d:
				checksum ^= ord(i) ''' 
			if checksum == byte:
				return list(self.d)
			else: 
				self.d.append(byte)
				self.d.popleft()

	def write(self, bytes):
		"takes byte[4], returns None" 
		if len(bytes) != 4:
			raise ValueError("Array is not 4 bytes long!")
                
		#checksum = 0
		for i in bytes:
			self.ser.write(i)
			#checksum ^= ord(i) '''
                checksum = hashlib.md5("".join(bytes) + chr(self.counter)).digest()[0]
                self.ser.write(chr(self.counter))
                # checksum ^= self.counter
		self.ser.write(checksum)
		self.counter = (self.counter + 1) % 256
		#print("Wrote", bytes, (self.counter - 1) % 256, checksum)
