import json

import socketio
from aiohttp import web


class SocketIOClient(socketio.AsyncClientNamespace):
  def __init__(self):
    super().__init__()
    self.sio = socketio.AsyncClient()
    self.sio.register_namespace(self)
    self.delegate = None

  async def run(self):
    await self.sio.connect('http://localhost:3000')
    await self.sio.wait()

  async def on_connect(self):
    print('connect')
    data = {
      "type": 6,
      "data": {
        "role": "wall-e"
      }
    }
    await self.sio.emit("message", json.dumps(data))

  def on_disconnect(self):
    print('disconnect')

  def on_message(self, message):
    print(self.delegate, message)
    if self.delegate is not None:
      self.delegate.handle_message(message)
    return 'OK'


if __name__ == '__main__':
  sioServer = SocketIOClient()
  sioServer.run()
