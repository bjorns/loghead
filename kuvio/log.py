"""
Logs filter and augment messages
"""
from .event import Event
from .format import Format, SimpleFormat
from .level import Level, DEBUG, INFO, NOTICE, WARNING, ERROR
from .drain import Drain, StderrDrain


class Log:
    def __init__(self):
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
    def __init__(self, name: str, level: Level = None, drain: Drain = None, f: Format = None):
        super(LogPipeline, self).__init__()
        self.name = name
        self.level = level
        if self.level is None:
            self.level = INFO

        self.drain = drain
        if not self.drain:
            self.drain = StderrDrain()

        self.format = f
        if not self.format:
            self.format = SimpleFormat()

    def log(self, level: int, msg: str):
        e = Event(level, msg)
        line = self.format.format(e)
        self.drain.write(line)

    def update(self, new_log):
        assert self.name == new_log.name
        self.level = new_log.level
        self.drain = new_log.drain
        self.format = new_log.format

    def __repr__(self) -> str:
        return f"LogPipeline<{self.name},{self.level.name},{self.format.name},{self.drain.name}>"
