"""
A filter can modify or terminate an event

"""
from .event import Event
from .level import Level
from .error import UnimplementedError


class Status:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"status:{self.name}"


TERMINATED = Status("terminated")
PROCESSED = Status("processed")
ERROR = Status("error")


class Filter:
    def __init__(self, name: str):
        self.name = name

    def process(self, event: Event) -> Status:
        raise UnimplementedError()

    def __repr__(self):
        return f"filter:{self.name}"


class LevelFilter(Filter):
    """
    The level filter terminates all log events that have a lower level than the predefined cutoff
    """

    def __init__(self, cutoff: Level):
        super(LevelFilter, self).__init__('status')
        self.cutoff = cutoff

    def process(self, event: Event) -> Status:
        if event.level >= self.cutoff:
            return PROCESSED
        else:
            return TERMINATED
