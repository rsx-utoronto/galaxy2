import serial
from collections import deque

class PacketSerial():
	""" 
	Really hack class to write 4 serial packets at once.
	Note that the packets are not checked for orer. 
	Read and write both take 4 bits at once
	"""
	def __init__(self, serial_connection):	
		self.ser = serial_connection
		self.d = deque(["a", "a", "a", "a"]) 

	def read(self):
		"returns byte[4] or None"
		for i in range(4):
			byte = self.ser.read()	
			
			if byte is None or byte == "":
			    return None

			# check whether it's a checksum packet
			checksum = 0
			for i in self.d:
				checksum ^= ord(i)
			if checksum == byte:
				return list(self.d)
			else: 
				self.d.append(byte)
				self.d.popleft()

	def write(self, bytes):
		"takes byte[4], returns None" 
		if len(bytes) != 4:
			raise ValueError("Array is not 4 bytes long!")

		checksum = 0
		for i in bytes:
			self.ser.write(i)
			checksum ^= ord(i)
		self.ser.write(chr(checksum))
		
