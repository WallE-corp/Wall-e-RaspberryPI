from SocketServerController import SocketServerController

class WallE(object):
    def left(self):
        print("WallE Left")

    def right(self):
        print("WallE right")

    def backward(self):
        print("WallE Backward")

    def forward(self):
        print("WallE Forawrd")


controller = SocketServerController()
walle = WallE()
controller.wallEDelegate = walle