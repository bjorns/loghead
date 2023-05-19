"""
Define "Writer" classes, these are objects responsible for writing formatted log
messages to a drain stream. This could be a file or stderr e.g.
"""
from io import TextIOWrapper
from sys import stderr

from .error import BaseclassError


class Drain:
    """
    Generic baseclass for drain classes
    """
    def __init__(self):
        self.name = "null"

    def write(self, msg: str):
        """
        Write a message to the drain. Message is assumed to be preformatted
        using a Format object.
        """
        raise BaseclassError("Not implemented")


class TextIODrain(Drain):
    """
    TextIO is the python version of a C++ stream. It's what open() returns and it's the
    type of stderr/stdout.
    """

    def __init__(self, f: TextIOWrapper):
        super().__init__()
        self.name = 'textio'
        self.f = f

    def write(self, msg: str):
        self.f.write(msg)
        self.f.write("\n")


class StderrDrain(TextIODrain):
    """
    Write log messages to STDERR
    """

    def __init__(self):
        super().__init__(stderr)
        self.name = 'stderr'
