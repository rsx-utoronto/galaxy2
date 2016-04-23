import serial
from collections import deque
import hashlib

class PacketSerial():
	""" 
	Really hack class to write 5 serial packets at once.
	Note that the packets are not checked for orer. 
	Read and write both take 5 bits at once
	"""
	def __init__(self, serial_connection):	
		self.ser = serial_connection
		self.d = deque(["a", "a", "a", "a", "a", "a"])
		self.counter = 0 # make packets unique

	def read(self):
		"returns byte[5] or None"

		for i in range(7):
			byte = self.ser.read()	
			if byte is None or byte == "":
			    return None
			# check whether it's a checksum packet
			checksum = hashlib.md5("".join(self.d)).digest()[0]
			'''checksum = 0
			for i in self.d:
				checksum ^= ord(i) ''' 
			if checksum == byte:
                                print(list(self.d), checksum)
				return list(self.d)
			else: 
				self.d.append(byte)
				self.d.popleft()

	def write(self, bytes):
		"takes byte[5], returns None" 
		if len(bytes) != 5:
			raise ValueError("Array is not 5 bytes long!")
                
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
		
	def available(self):
		"""Returns whether a packet can be read. Does not guarantee
		that the packet will be valid """
		return self.ser.in_waiting >= 7
