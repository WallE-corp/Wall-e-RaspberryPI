#!/usr/bin/env python3

import serial
from walle_networking import WallECommandHandler

ch = WallECommandHandler()

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()


@ch.move('left')
def left(data):
  print('Left command', data)
  ser.write(b"left\n")


@ch.move('right')
def right(data):
  print('Right command', data)
  ser.write(b"right\n")


@ch.move('forward')
def forward(data):
  print('Forward command', data)
  ser.write(b"go\n")


@ch.move('backward')
def backward(data):
  print('Backward command', data)
  ser.write(b"back\n")


if __name__ == '__main__':
  ch.start_listening()
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
