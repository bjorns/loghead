from contextlib import contextmanager
from io import StringIO
from unittest.mock import patch
from tempfile import mkstemp
from os import remove

from pytest import raises

from loghead.drain import Drain, TextIODrain, StderrDrain, FileDrain
from loghead.error import BaseclassError


def test_write_to_baseclass_throws():
    with raises(BaseclassError):
        d = Drain()
        assert d.name == 'null'
        d.write("test")


def test_textio_drain():
    buf = StringIO()
    d = TextIODrain(f=buf)
    assert d.name == 'textio'
    d.write("test")
    assert buf.getvalue() == "test\n"


@patch('loghead.drain.stderr', new_callable=StringIO)
def test_stderr_drain(stderr: StringIO):
    d = StderrDrain()
    d.write("hello stderr")
    assert stderr.getvalue() == "hello stderr\n"


@contextmanager
def tempfile(suffix: str):
    filename = None
    try:
        _, filename = mkstemp(suffix=suffix, prefix='loghead-')
        yield filename
    finally:
        if filename:
            remove(filename)


def test_file_drain():
    with tempfile(suffix='-test-file-drain.log') as filename:
        d = FileDrain(filepath=filename)
        assert str(d) == f"file:{filename}"
        assert repr(d) == f"loghead.drain.StderrDrain<file:{filename}>"
        d.write("hello world")
        d.close()
        with open(filename) as f:
            file_content = str(f.read())
            assert file_content == "hello world\n"

