"""
Logs filter and augment messages
"""
from .event import Event
from .format import Format, SimpleFormat
from .level import DEBUG, INFO, NOTICE, WARNING, ERROR
from .write import Writer, StderrWriter


class Log:
	def __init__(self, msg: str):
		pass

	def debug(self, msg: str):
		self.log(DEBUG, msg)

	def info(self, msg: str):
		self.log(INFO, msg)

	def notice(self, msg: str):
		self.log(WARNING, msg)

	def warning(self, msg: str):
		self.log(WARNING, msg)

	def error(self, msg: str):
		self.log(ERROR, msg)

	def log(self, level: int, msg: str):
		pass


class LogPipeline(Log):
	def __init__(self, w: Writer=None, f: Format=None):
		self.writer = w
		if not self.writer:
			self.writer = StderrWriter()
		self.format = f
		if not self.format:
			self.format = SimpleFormat()

	def log(self, level: int, msg: str):
		e = Event(level, msg)
		line = self.format.format(e)
		self.writer.write(line)
