"""
Logs filter and augment messages
"""
from .event import Event
from .format import Format, SimpleFormat
from .level import Level, DEBUG, INFO, NOTICE, WARNING, ERROR
from .write import Writer, StderrWriter


class Log:
    def __init__(self, msg: str):
        pass

    def update(self, new_log):
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
    def __init__(self, name: str, level: Level, w: Writer = None, f: Format = None):
        self.name = name
        self.level = level

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

    def update(self, new_log: Log):
        assert self.name == new_log.name
        self.level = new_log.level
        self.writer = new_log.writer
        self.format = new_log.format
