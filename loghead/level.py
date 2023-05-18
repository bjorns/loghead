"""
We redefine the log levels to line up with logging package just in case.
We add one extra level NOTICE which is for important but non-error related
messages.
"""
from .error import UserError
from functools import total_ordering


@total_ordering
class Level:
    def __init__(self, value: int, name: str):
        assert name.isalpha()
        assert name.islower()
        self.name = name
        assert value <= 100
        assert value > 0
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return f"{self.name}({self.value})"


DEBUG = Level(10, 'debug')
INFO = Level(20, 'info')
NOTICE = Level(25, 'notice')
WARNING = Level(30, 'warning')
ERROR = Level(40, 'error')
FATAL = Level(50, 'fatal')
DISABLED = Level(100, 'disabled')

ALL_LEVELS = [
    DEBUG,
    INFO,
    NOTICE,
    WARNING,
    ERROR,
    FATAL,
    DISABLED
]

LEVEL_BY_NAME = {l.name: l for l in ALL_LEVELS}


def get_level(name: str) -> Level:
    ret = LEVEL_BY_NAME.get(name)
    if ret is None:
        names = LEVEL_BY_NAME.keys()
        raise UserError(
            f"Requested level {name} not found, available: {', '.join(names)}")
    return ret
