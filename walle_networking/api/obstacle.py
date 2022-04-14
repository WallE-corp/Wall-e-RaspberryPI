from src.api.backend_requests import base_url, timeout
from dataclasses import dataclass
import requests
import pickle
import os
import inspect


obstacle_events = []
unsynced_obstacle_events = []

@dataclass
class ObstacleEvent:
  """
  Represents an obstacle event.

  Attributes:
  -----------
  vx: int
    The virtual x coordinate of the obstacle.
  vy: int
    The virtual y coordinate of the obstacle.
  obstacle_image_filepath: str
    The file path of the obstacle image.
  is_uploaded: bool
    Whether the obstacle event has been uploaded to the backend.
  """
  vx: int
  vy: int
  obstacle_image_filepath: str
  is_uploaded: bool = False

  def get_dict(self):
    return {
      'vx': self.vx,
      'vy': self.vy,
      'obstacle_image_filepath': self.obstacle_image_filepath
    }

  def __str__(self) -> str:
    return f'ObstacleEvent(vx={self.vx}, vy={self.vy}, obstacle_image_filepath={self.obstacle_image_filepath}, is_uploaded={self.is_uploaded})'


def store_unsynced_obstacle_events():
  """
  Stores all unsynced obstacle events to a file.

  Returns:
  --------
    Boolean on whether the unsynced obstacle events were successfully stored.
  """
  try:
    curdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    with open(curdir + '\\data\\obstacle_events.pkl', 'wb') as f:
      pickle.dump(unsynced_obstacle_events, f)
    return True
  except Exception as e:
    print(e)
    return False


def upload_obstacle_event(obstacle_event: ObstacleEvent):
  """
  Locally stores an ObstacleEvent then attempts to upload
  it to the backend server.

  Args:
  obstacle_event: ObstacleEvent
    The obstacle event to upload.

  Returns:
    Boolean on whether the ObstacleEvent was successfully uploaded to the backend.
  """
  # Push event to obstacle_events list
  obstacle_events.append(obstacle_event)

  # Attempt to upload event to backend
  image_fd = open(obstacle_event.obstacle_image_filepath, 'rb')
  image_binary = image_fd.read()
  image_fd.close()

  request_files = {'image': image_binary}
  request_payload = obstacle_event.get_dict()

  was_successful = False
  try:
    response = requests.put(base_url + '/obstacle_events', files=request_files, data=request_payload)
    if response.status_code == 201:
      print('Successfully uploaded obstacle event to backend.')
      was_successful = True
  except Exception as e:
    print(e)

  if not was_successful:
    print('Failed to upload obstacle event to backend.')
    unsynced_obstacle_events.append(obstacle_event)
    store_unsynced_obstacle_events()

  return True
