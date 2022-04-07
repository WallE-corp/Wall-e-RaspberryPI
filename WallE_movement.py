
#!/usr/bin/env python3

import serial
import time
from SocketServerController import SocketServerController

class WallE(object):
    def __init__(self):
        print("init")
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        self.ser.reset_input_buffer()
        print("mino")
        self.controller = SocketServerController()
        self.controller.wallEDelegate = self
        print("meep")
        
    def forward(self):
        self.ser.write(b"go\n")
        
    
    def backward(self):
        self.ser.write(b"back\n")
    
    def left(self):
        self.ser.write(b"left\n")
    
    def right(self):
        self.ser.write(b"right\n")

if __name__ == '__main__':
    print("meep")
    walle = WallE()
    """
	ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
	ser.reset_input_buffer()
	data = 0
	while True:
		if data == 0:
			ser.write(b"go\n")
			data = 1
		elif data == 1:
			ser.write(b"back\n")
			data = 0
		line = ser.readline().decode('utf-8').rstrip()
		print(line)
		time.sleep(3)
		"""
