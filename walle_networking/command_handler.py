import json
from enum import IntEnum
from src.socketio_client import SocketIOClient


class Commands(IntEnum):
  MOVEMENT = 4
  START_CALIBRATION = 5


class WallECommandHandler(object):
  def __init__(self):
    self.sio_server = SocketIOClient()
    self.sio_server.delegate = self

    self.commands = {
      Commands.MOVEMENT: self.handle_movement_command
    }
    self.movement_commands = {}

  async def start_listening(self):
    await self.sio_server.run()

  def handle_message(self, message):
    try:
      message_data = json.loads(message)
      command = self.commands.get(message_data['type'])
      command(message_data['data'])
      return True
    except Exception as e:
      print('Could not execute handle_message.', e)
      return False

  def handle_movement_command(self, data):
    try:
      movement = data['movement']
      movement_command = self.movement_commands.get(movement)
      movement_command(data['action'])
      return True
    except Exception as e:
      print('Could not execute handle_movement_command.', e)
      return False

  # ======= Decorator functions ===================
  def move(self, movement):
    def decorator_move(func):
      self.movement_commands[movement] = func
    return decorator_move

  def command(self, command_type):
    def decorator_command(func):
      self.commands[command_type] = func
    return decorator_command

