from command_handler import WallECommandHandler

ch = WallECommandHandler()


@ch.move('left')
def left(data):
  print('Left command', data)


@ch.move('right')
def right(data):
  print('Right command', data)


@ch.move('forward')
def forward(data):
  print('Forward command', data)


@ch.move('backward')
def backward(data):
  print('Backward command', data)


ch.start_listening()