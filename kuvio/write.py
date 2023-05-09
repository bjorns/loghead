"""
Define "Writer" classes, these are objects responsible for writing formatted log
messages to a drain stream. This could be a file or stderr e.g.
"""
from io import TextIOBase
from sys import stderr


class Writer:
    def write(self, msg: bytes):
        raise Exception("Not implemented")


class TextIOWriter(Writer):
    """
    TextIO is the python version of a C++ stream. It's what open() returns and it's the
    type of stderr/stdout.
    """

    def __init__(self, f: TextIOBase):
        self.f = f

    def write(self, msg: str):
        self.f.write(msg)
        self.f.write("\n")


class StderrWriter(TextIOWriter):
    """
    Write log messages to STDERR
    """

    def __init__(self):
        super(StderrWriter, self).__init__(stderr)
