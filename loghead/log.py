"""
Logs are the main interface for users to interact with the package.
"""
from datetime import datetime

from .event import Event
from .error import UserError, BaseclassError
from .filter import Filter, LevelFilter, TERMINATED
from .format import Format, SimpleFormat
from .level import Level, DEBUG, INFO, NOTICE, WARNING, ERROR
from .drain import Drain, StderrDrain


class Log:
    """
    Base class for log implementations
    """

    def __init__(self):
        pass

    def update(self, new_log):
        """
        merge new_log object properties into self
        """
        raise BaseclassError("Log does not implement update()")

    def debug(self, msg: str):
        """
        Write debug message to log
        """
        self.log(DEBUG, msg)

    def info(self, msg: str):
        """
        Write info message to log
        """
        self.log(INFO, msg)

    def notice(self, msg: str):
        """
        Write notice message to log
        """
        self.log(NOTICE, msg)

    def warning(self, msg: str):
        """
        Write warning message to log
        """
        self.log(WARNING, msg)

    def error(self, msg: str):
        """
        Write error message to log
        """
        self.log(ERROR, msg)

    def log(self, level: Level, msg: str):
        """
        Write message to log
        """
        raise BaseclassError(f"Log {self} does not implement log()")

    def get_level(self) -> Level:
        """
        get_level() is a convenience method allowing a user to query the log
        what level it is expecting to log on.
        """
        raise BaseclassError(f"Log {self} does not have a level")

    def get_format(self) -> str:
        """
        Get the current format name from the log
        """
        raise BaseclassError(f"Log {self} does not have a format")


class LogPipeline(Log):
    """
    LogPipeline is a flexible log implementation. It uses submodules to implement all functionality
    as a pipeline of events that filter and then output events. The process is:

    - A set of filters modify or filter out events based on e.g. level
    - A formatter converts the event into a bytestream (string)
    - A set of writers write the event to some output stream.

    The log pipeline has a set of default settings so:

        LogPipeline("ny-log")

    is equivalent to:

        LogPipeline("my-log", LevelFilter(INFO),  SimpleFormat(), StderrDrain())

    """

    def __init__(self, name: str, *components):
        super().__init__()
        self.name = name
        self.filters = list()
        self.format = None
        self.drains = list()

        for component in components:
            if issubclass(type(component), Filter):
                self.filters.append(component)
            elif issubclass(type(component), Format):
                if self.format is not None:
                    raise UserError(f"A log pipeline cannot have two formats: {self.format} and "
                                    f"{component}")
                self.format = component
            elif issubclass(type(component), Drain):
                self.drains.append(component)
            else:
                raise UserError(f"Object {component}({type(component)}) "
                                f"is not a supported component")

        if len(self.filters) == 0:
            self.filters.append(LevelFilter(INFO))

        # If user has supplied no formatter, use a default
        if self.format is None:
            self.format = SimpleFormat()

        # If user has supplied no drain, use stderr as default
        if len(self.drains) == 0:
            self.drains.append(StderrDrain())

    def log(self, level: Level, msg: str):
        event = Event(level, msg)

        for flt in self.filters:
            if flt.process(event) == TERMINATED:
                return

        line = self.format.format(event)
        print(self.drains)
        for drain in self.drains:
            drain.write(line)

    def update(self, new_log):
        assert self.name == new_log.name
        self.filters = new_log.filters
        self.format = new_log.format
        self.drains = new_log.drains

    def get_level(self) -> Level:
        """
        get_level() is a convenience method allowing a user to query the log
        what level it is expecting to log on.
        Note that it is low performance and should not be called in a running
        program other than for debugging or setup logic.
        """
        for f in self.filters:
            if isinstance(f, LevelFilter):
                level_filter: LevelFilter = f
                return level_filter.cutoff
        raise UserError(f"{self} does not have a level filter defined and cannot so does not define a level.")

    def get_format(self) -> str:
        if self.format:
            return self.format.name
        raise BaseclassError(f"Log {self} does not have a format")

    def __repr__(self) -> str:
        return f"LogPipeline<{self.name}>"
