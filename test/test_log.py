from pytest import raises
from loghead.log import Log
from loghead.error import BaseclassError


def test_log_throws():
    for level in ['debug', 'info', 'notice', 'warning', 'error']:
        with raises(BaseclassError):
            log = Log()
            if level == 'debug':
                log.debug("hello, world!")
            elif level == 'info':
                log.info("hello, world!")
            elif level == 'notice':
                log.notice("hello, world!")
            elif level == 'warning':
                log.warning("hello, world!")
            elif level == 'error':
                log.error("hello, world!")


def test_log_update_throws():
    with raises(BaseclassError):
        log = Log()
        new_log = Log()
        log.update(new_log)


def test_log_get_level_throws():
    with raises(BaseclassError):
        log = Log()
        log.get_level()


def test_log_get_format_throws():
    with raises(BaseclassError):
        log = Log()
        log.get_format()
