"""
Logs filter and augment messages
"""
from .write import Writer, StderrWriter
from .level import DEBUG, INFO, NOTICE, WARNING, ERROR

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
	def __init__(self, w: Writer=None):
		self.writer = w
		if not self.writer:
			self.writer = StderrWriter()

	def log(self, level: int, msg: str):
		self.writer.write(msg)
