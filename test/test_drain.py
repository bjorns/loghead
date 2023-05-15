from io import StringIO
from unittest.mock import patch

from pytest import raises

from kuvio.drain import Drain, TextIODrain, StderrDrain
from kuvio.error import BaseclassError


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


@patch('kuvio.drain.stderr', new_callable=StringIO)
def test_stderr_drain(stderr: StringIO):
    d = StderrDrain()
    d.write("hello stderr")
    assert stderr.getvalue() == "hello stderr\n"
