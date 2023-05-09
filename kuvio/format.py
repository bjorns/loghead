"""

"""
from .event import Event


class Format:
    def __init__(self):
        pass

    def format(self, e: Event) -> str:
        pass


class SimpleFormat(Format):
    def __init__(self):
        super(SimpleFormat, self).__init__()

    def format(self, e: Event) -> str:
        return f"{e.level.name}: {e.msg}"
