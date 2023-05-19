"""
The log event captures the full context of the log invocation
"""
from datetime import datetime

from .level import Level

_local_tz = datetime.utcnow().astimezone().tzinfo


class Event:
    """
    Represents a log event, created automatically by the Log implementation. In
    the LogPipeline it's created and then passed through all components during
    processing.
    """
    def __init__(self, level: Level, msg: str):
        self.timestamp = datetime.now(_local_tz)
        self.level = level
        self.msg = msg
