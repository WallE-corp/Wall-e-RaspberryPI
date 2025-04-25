from walle_networking import SocketIOServer

class SocketHandler:
  def __init__(self):
    self.sioServer = SocketIOServer()
    self.sioServer.delegate = self
    self.sioServer.run()

  def handle_message(self, message):
    print(message)


sh = SocketHandler()
