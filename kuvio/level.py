"""
We redefine the log levels to line up with logging package just in case.
We add one extra level NOTICE which is for important but non-error related
messages.
"""

class Level:
	def __init__(self, value: int, name: str):
		assert name.isalpha()
		assert name.islower()
		self.name = name
		assert value <= 100
		assert value > 0
		self.value = value

DEBUG = Level(10, 'debug')
INFO = Level(20, 'info')
NOTICE = Level(25, 'notice')
WARNING = Level(30, 'warning')
ERROR = Level(40, 'error')
FATAL = Level(50, 'fatal')
DISABLED = Level(100, 'disabled')
