"""

"""
from json import dumps as jsondump
from .event import Event


class Format:
    def __init__(self):
        self.name = 'null'

    def format(self, e: Event) -> str:
        pass


class SimpleFormat(Format):
    def __init__(self):
        super(SimpleFormat, self).__init__()
        self.name = 'simple'

    def format(self, e: Event) -> str:
        return f"{e.timestamp.isoformat()} {e.level.name}: {e.msg}"


class SimpleJsonFormat(Format):
    def __init__(self):
        super(SimpleJsonFormat, self).__init__()
        self.name = 'json'

    def format(self, e: Event):
        return f"{{\"time\":{jsondump(e.timestamp.isoformat())},\"message\":{jsondump(str(e.msg))}}}"
