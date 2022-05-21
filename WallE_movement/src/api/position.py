from src.api.backend_requests import base_url, timeout
import requests
import threading
import time

x = 0.0
y = 0.0
l_x = 0.0
l_y = 0.0




def current_mili_time():
    return (time.time() * 1000)

last_handle_time = current_mili_time()

def upload_position_data():
  """
  Attempts to upload position data to the backend
  Args:
    data: object
      Object containing at minimum the x and y position data to upload.

  Returns:
    True if the data was successfully uploaded
  """
  global x, y
  data = {
    "x": x,
    "y": y
  }
  res = requests.post(f'{base_url}/pathpoints', data)
  if res.status_code >= 500:
    return False
  x = 0
  y = 0
  return True


def handle_position_data(_x, _y):
  """
  Adds the give x, y data to a local x, y which is then uploaded at next interval

  """

  global x, y, last_handle_time, l_x, l_y
  

  current_handle_time = current_mili_time()
  
  dt = current_handle_time - last_handle_time # Time difference in miliseconds
  dt = dt / 1000 # Time difference in seconds
  # (l_x, l_y) is the velocity vector cm/s
  # multiply by dt to get the actual moved position
  a_x = dt * l_x
  a_y = dt * l_y

  
  # Add on the acutal moved distance
  x += float(a_x)
  y += float(a_y)
  
  last_handle_time = current_mili_time()
  # Saved _x, _y so we can check next time
  l_x = float(_x)
  l_y = float(_y)

def start_uploading_position_data(interval):
  """
  Starts uploading position data on separate thread at the interval
  provided in arguments.
  Args:
    interval: number
      Rate in seconds at which to upload position data
  """
  upload_position_data()
  threading.Timer(interval, start_uploading_position_data, [interval]).start()
  

start_uploading_position_data(1)
