import socketio
from aiohttp import web


class SocketIOServer(socketio.AsyncNamespace):
  def __init__(self):
    super().__init__()
    self.sio = socketio.AsyncServer()
    self.sio.register_namespace(self)
    self.app = web.Application()
    self.sio.attach(self.app)
    self.delegate = None

  def run(self):
    web.run_app(self.app, port=8080)

  def on_connect(self, sid, environ):
    print('connect', sid)

  def on_disconnect(self, sid):
    print('disconnect', sid)

  def on_message(self, sid, message):
    print(self.delegate, message)
    if self.delegate is not None:
      self.delegate.handle_message(message)
    return 'OK'