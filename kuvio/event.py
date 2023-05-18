"""
The log event captures the full context of the log invocation
"""
from datetime import datetime

from .level import Level

_local_tz = datetime.utcnow().astimezone().tzinfo


class Event:
    def __init__(self, level: Level, msg: str):
        self.timestamp = datetime.now(_local_tz)
        self.level = level
        self.msg = msg
