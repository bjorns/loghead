"""
Define "Writer" classes, these are objects responsible for writing formatted log
messages to a drain stream. This could be a file or stderr e.g.
"""
from datetime import datetime
from io import TextIOWrapper
from sys import stderr

from .error import BaseclassError


class Drain:
    """
    Generic baseclass for drain classes
    """

    def __init__(self):
        self.name = "null"

    def __del__(self):
        self.close()

    def write(self, msg: str):
        """
        Write a message to the drain. Message is assumed to be preformatted
        using a Format object.
        """
        raise BaseclassError("Not implemented")

    def close(self):
        """
        Close any underlying resources
        """


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


class FileDrain(TextIODrain):
    """
    A file writing drain
    """

    def __init__(self, filepath: str):
        self.created = datetime.now()
        # pylint: disable=consider-using-with
        self.f = open(filepath, 'a', encoding='utf-8')
        super().__init__(self.f)
        self.name = f"file:{filepath}"

    def write(self, msg: str):
        super().write(msg)
        self.f.flush()

    def close(self):
        """
        Close the underlying file
        """
        if self.f is not None:
            self.f.close()
            self.f = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"loghead.drain.StderrDrain<{self.name}>"
