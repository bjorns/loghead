from pytest import raises

from kuvio.level import INFO
from kuvio.drain import Drain, TextIODrain, StderrDrain
from kuvio.error import BaseclassError


def test_write_to_baseclass_throws():
    with raises(BaseclassError):
        d = Drain()
        d.write("test")
