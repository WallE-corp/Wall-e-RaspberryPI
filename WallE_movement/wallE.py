#!/usr/bin/env python3
from picamera import PiCamera
import asyncio
import serial
import time
import requests
import threading
from src.api.position import *
from src.api.obstacle import *
from src.command_handler import *

camera = PiCamera()
file_name ="/home/pi/Pictures/img_"+ str(time.time()) + ".jpg"
command = "Stop"
obstacle_detected = False
old_command = command
ch = WallECommandHandler()

@ch.move('forward')
def forward (action):
    global command
    if action == "start":
        command = "Forward"
    else:
        command = "Stop"
        
@ch.move('backward')
def backward (action):
    global command
    if action == "start":
        command = "Backward"
    else:
        command = "Stop"
    
@ch.move('left')
def left (action):
    global command
    if action == "start":
        command = "Left"
    else:
        command = "Stop"
        
@ch.move('right') 
def right (action):
    global command
    if action == "start":
        command = "Right"
    else:
        command = "Stop"
        
@ch.command(10)
def auto (data):
    global command
    print(data)
    if data["action"] == "start":
        command = "Auto"
    else:
        command = "Stop"
    

def main():
    global old_command, obstacle_detected  
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()
    print("Starting serial loop")
    while True:
        
        if command != old_command:
            print("Sending new command")
            if command == "Stop":
                ser.write(b"Stop\n")
            elif command == "Left":
                ser.write(b"Left\n")
            elif command == "Right":
                ser.write(b"Right\n")
            elif command == "Forward":
                ser.write(b"Forward\n")
            elif command == "Backward":
                ser.write(b"Backward\n")
            elif command == "Auto": 
                ser.write(b"Auto\n")
            
            old_command = command
            
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            line_split = line.split(",")
            xDistance = line_split[1]
            yDistance = line_split[2]
 
            handle_position_data(xDistance, yDistance)
            if line_split[0] == "Object detected" and not obstacle_detected:
                print("uploading object event")
                camera.capture(file_name)
                obstacle_event = ObstacleEvent(vy=float(yDistance), vx=float(xDistance), obstacle_image_filepath=file_name)
                upload_obstacle_event(obstacle_event)
                obstacle_detected = True
            elif line_split[0] == "No object detected" and obstacle_detected:
                obstacle_detected = False
                            

if __name__ == "__main__":
    t = threading.Thread(target=main)
    t.start()
    start_uploading_position_data(1)
    asyncio.run(ch.start_listening())