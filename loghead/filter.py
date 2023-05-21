"""
A filter can modify or terminate an event
"""

from .event import Event
from .level import Level
from .error import UnimplementedError


class Status:
    """
    The status of the
    """
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"status:{self.value}"


TERMINATED = Status("terminated")
PROCESSED = Status("processed")
ERROR = Status("error")


class Filter:
    """
    Filter and process events
    """
    def __init__(self, name: str):
        self.name = name

    def process(self, event: Event) -> Status:
        """
        Modify or terminate events
        :return: a status signifies if processing succeeeded or terminated the event in which case it
        will not be further processed or output.
        """
        raise UnimplementedError()

    def __repr__(self):
        return f"filter:{self.name}"


class LevelFilter(Filter):
    """
    The level filter terminates all log events that have a lower level than the predefined cutoff
    """

    def __init__(self, cutoff: Level):
        super().__init__('status')
        self.cutoff = cutoff

    def process(self, event: Event) -> Status:
        """
        If the event is equal or higher level to the filters cutoff, it will return PROCESSED.
        if the event has a lower level (e.g. DEBUG is lower than INFO) it will be TERMINATED.
        """
        if event.level >= self.cutoff:
            return PROCESSED
        else:
            return TERMINATED
