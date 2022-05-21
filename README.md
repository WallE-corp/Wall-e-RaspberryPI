# Wall-e-RaspberryPI

### Setting up for the Raspberry Pi: ###
1. Download and install Raspberry pi Imager on the computer.
2. Insert a microSD card into the computer
3. Click Choose OS and select Raspberry Pi OS
4. Click Choose SD card.
5. Click Write
6. Connect HDMI cable to the screen →  connect power supply to Raspberry Pi

### Setting up the camera: ###
1. Connect the camera in Raspberry Pi
2. From Raspberry Pi terminal, run sudo raspi-config
3. Select “Navigate to interface options” → “legacy camera” → enable → yes
4. Select finish and reboot the Raspberry Pi
5. In [python IDE] or terminal, install the following: 
    * sudo apt-get update
    * sudo apt-get upgrade
    * pip3 install picamera
6. From Raspberry Pi terminal, run vcgencmd get_camera. If you get (supported=1 detected=1), that's mean your camera is connected successfully

### Setting up the socket: ###
In [python IDE] or terminal, install the following:
    * pip install python-socketio

