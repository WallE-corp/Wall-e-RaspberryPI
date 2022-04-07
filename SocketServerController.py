from SocketServer import SocketServer
from threading import Timer
import json


class SocketServerController(object):
    def __init__(self):
        self.socketServer = SocketServer()
        self.socketServer.delegate = self
        self.socketServer._messenger.messageDelegate = self
        self.wallEDelegate = None

        if self.socketServer.connect():
            self.timer = Timer(self.socketServer.pollFreq / 1000, self.pollMessages)
            self.timer.start()

    def pollMessages(self):
        if self.socketServer.running:
            del self.timer
            self.timer = Timer(self.socketServer.pollFreq / 1000, self.pollMessages)
            self.timer.start()
            self.socketServer.pollMessages()

    def message(self, msg):
        messageDict = json.loads(msg)
        if messageDict["type"] == 4 and self.wallEDelegate is not None:
            command = messageDict["command"]
            if command == "left":
                print("Turn left")
                self.wallEDelegate.left()
                pass
            elif command == "right":
                print("Turn right")
                self.wallEDelegate.right()
                pass
            elif command == "backward":
                print("Move backward")
                self.wallEDelegate.backward()
                pass
            elif command == "forward":
                print("Move forward")
                self.wallEDelegate.forward()
                pass
            else:
                print("Unkown command")


    def clientConnected(self, clientId):
        print("Client connected")

    def clientDisconnectedAtIndex(self, index):
        print("Client disconnected")