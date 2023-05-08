"""
The log event captures the full context of the log invocation
"""
from .level import Level

class Event:
	def __init__(self, level: Level, msg: str):
		self.level = level
		self.msg = msg
