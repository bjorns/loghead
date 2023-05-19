"""
The formatter takes an Event object and renders a log line as a string
"""
from json import dumps as jsondump
from .event import Event
from .error import BaseclassError


class Format:
    """
    Baseclass for Formatters. The formatter takes an Event object and renders a
    log line as a string
    """
    def __init__(self):
        self.name = 'null'

    def format(self, _: Event) -> str:
        """
        Convert an Event object to a log line string
        """
        raise BaseclassError("Baseclass {self} does not implement format")


class SimpleFormat(Format):
    """
    The simplest possible formatter with a hard coded single line compact format
    for local running and testing
    """
    def __init__(self):
        super().__init__()
        self.name = 'simple'

    def format(self, event: Event) -> str:
        """
        Convert an Event object to a log line string
        """
        timestamp = event.timestamp.strftime("%H:%M:%S")
        return f"{timestamp} {event.level.name}: {event.msg}"


class SimpleJsonFormat(Format):
    """
    A simple compact JSON format
    """
    def __init__(self):
        super().__init__()
        self.name = 'json'

    def format(self, event: Event):
        """
        Convert an Event object to a log line string
        """
        timestamp = jsondump(event.timestamp.isoformat())
        return f"{{\"time\":{timestamp},\"message\":{jsondump(str(event.msg))}}}"
