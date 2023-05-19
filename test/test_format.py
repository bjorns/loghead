from datetime import datetime
from unittest.mock import patch, Mock

from pytest import raises

from loghead.event import Event
from loghead.error import BaseclassError
from loghead.format import Format, SimpleFormat, SimpleJsonFormat
from loghead.level import INFO


def test_baseclass_throws():
    with raises(BaseclassError):
        f = Format()
        e = Event(INFO, "hello, world!")
        f.format(e)


@patch('loghead.event.datetime')
def test_simpleformat_format(mock_datetime):
    now = datetime.now()
    mock_datetime.now = Mock(return_value=now)
    f = SimpleFormat()
    e = Event(INFO, "hello, world!")
    assert f.format(e) == f"{now.strftime('%H:%M:%S')} info: hello, world!"


@patch('loghead.event.datetime')
def test_simplejsonformat_foramt(mock_datetime):
    now = datetime.now()
    mock_datetime.now = Mock(return_value=now)
    f = SimpleJsonFormat()
    e = Event(INFO, "hello, world!")
    assert f.format(e) == f'{{"time":"{now.isoformat()}","message":"hello, world!"}}'
