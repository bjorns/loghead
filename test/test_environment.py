from loghead.environment import Environment, get_root_log, has_log, set_log, get_log, get_global_env
from loghead.log import LogPipeline


def test_root_log():
    e = Environment()
    assert e.get_root_log() is not None
    assert get_root_log() is not None


def test_setget_log():
    e = Environment()
    log_name = 'testlog'
    l = LogPipeline(log_name)
    assert not e.has_log(log_name)
    e.set_log(log_name, l)
    assert e.has_log(log_name)
    assert e.get_log(log_name) == l


def test_get_log_doesnt_exist():
    e = Environment()
    log_name = 'testlog'
    assert not e.has_log(log_name)
    assert e.get_log(log_name) == e.get_root_log()


def test_setget_global_log():
    log_name = 'testlog'
    l = LogPipeline(log_name)
    assert not has_log(log_name)
    set_log(log_name, l)
    assert has_log(log_name)
    assert get_log(log_name) == l


def test_global_env():
    assert get_global_env() is not None
