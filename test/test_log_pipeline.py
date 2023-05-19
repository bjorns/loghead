from datetime import datetime
from io import StringIO
from unittest.mock import patch, Mock

from pytest import raises

from loghead.drain import TextIODrain, StderrDrain
from loghead.error import UserError
from loghead.event import Event
from loghead.filter import Filter, LevelFilter, Status, PROCESSED
from loghead.format import SimpleFormat, SimpleJsonFormat
from loghead.level import INFO, WARNING, ALL_LEVELS
from loghead.log import LogPipeline


@patch('loghead.event.datetime')
def test_standard_pipeline(mock_datetime):
    now = datetime.now()
    mock_datetime.now = Mock(return_value=now)
    buf = StringIO()

    log = LogPipeline('test-pipeline', LevelFilter(INFO), SimpleFormat(), TextIODrain(buf))

    log.debug("debug logs are filtered")
    log.info("hello world")

    assert buf.getvalue() == f"{now.strftime('%H:%M:%S')} info: hello world\n"


@patch('loghead.event.datetime')
def test_force_level_filter(mock_datetime):
    now = datetime.now()
    mock_datetime.now = Mock(return_value=now)
    buf = StringIO()

    # No level filter is defined
    log = LogPipeline('test-pipeline', SimpleFormat(), TextIODrain(buf))

    log.debug("debug logs are filtered")
    log.info("hello world")

    assert buf.getvalue() == f"{now.strftime('%H:%M:%S')} info: hello world\n"
    assert log.get_level() == INFO


@patch('loghead.event.datetime')
def test_force_default_simpled_format(mock_datetime):
    now = datetime.now()
    mock_datetime.now = Mock(return_value=now)
    buf = StringIO()

    # No format defined
    log = LogPipeline('test-pipeline', LevelFilter(INFO), TextIODrain(buf))

    log.info("hello world")

    # Simple format is still deployed
    assert buf.getvalue() == f"{now.strftime('%H:%M:%S')} info: hello world\n"


def test_double_format_throws():
    with raises(UserError):
        LogPipeline('test-pipeline', LevelFilter(INFO), SimpleFormat(), SimpleJsonFormat())


def test_non_component_throws():
    with raises(UserError):
        LogPipeline('test-pipeline', LevelFilter(INFO), SimpleFormat(), Event(INFO, "test"))


@patch('loghead.event.datetime')
def test_update_log_pipeline(mock_datetime):
    now = datetime.now()
    mock_datetime.now = Mock(return_value=now)

    log1 = LogPipeline("test-pipeline", LevelFilter(INFO), SimpleJsonFormat(), StderrDrain())

    buf = StringIO()
    log2 = LogPipeline("test-pipeline", LevelFilter(WARNING), SimpleFormat(), TextIODrain(buf))

    log1.update(log2)

    assert log1.name == "test-pipeline"

    log1.warning("hello world")
    assert buf.getvalue() == f"{now.strftime('%H:%M:%S')} warning: hello world\n"


class NullFilter(Filter):
    def __init__(self):
        super(NullFilter, self).__init__('status')

    def process(self, event: Event) -> Status:
        return PROCESSED


def test_get_level():
    for level in ALL_LEVELS:
        log = LogPipeline('test-pipeline', LevelFilter(level))
        assert log.get_level() == level


def test_no_level_found():
    with raises(UserError):
        log = LogPipeline('test-pipeline', NullFilter(), SimpleFormat())
        log.get_level()


def test_get_format():
    log = LogPipeline('test-pipeline', SimpleFormat())
    assert log.get_format() == 'simple'


def test_no_format():
    with raises(UserError):
        log = LogPipeline('test-pipeline')
        log.format = None  # Unknown why a user would do this
        log.get_format()
