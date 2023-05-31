from pytest import raises

from loghead.config import Config, PipelineConfig, ConfigError, DrainConfig
from loghead.drain import StderrDrain, FileDrain
from loghead.environment import Environment
from loghead.factory import load_environment, load_drain
from loghead.level import DEBUG, INFO

DEFAULT_PIPELINE_NAME = 'test_pipeline'


def load_test_environment(pipeline_name=DEFAULT_PIPELINE_NAME, form='simple', level='info',
                          filepath='test/config/debug_log.yaml', global_env=False):
    p = PipelineConfig(name=pipeline_name, form=form, level=level)
    c = Config(filepath=filepath, pipelines=[p])
    e = None if global_env else Environment()
    return load_environment(c, env=e)


def test_load_basic_environment():
    e = load_test_environment()
    assert len(e.logs) == 2
    assert e.has_log('root')
    assert e.has_log(DEFAULT_PIPELINE_NAME)
    log = e.get_log(DEFAULT_PIPELINE_NAME)
    assert log.get_level() == INFO
    assert log.get_format() == 'simple'


def test_load_global_environment():
    """
    The global environment may have other logs from other tests.
    """
    e = load_test_environment(global_env=True)
    assert len(e.logs) >= 2
    assert e.has_log('root')
    assert e.has_log(DEFAULT_PIPELINE_NAME)


def test_load_environment_with_updated_config():
    """
    The global environment may have other logs from other tests.
    """
    pipeline_name = 'test_pipeline'
    p = PipelineConfig(name=pipeline_name, form='simple', level='info')
    c = Config(filepath="test/config/debug_log.yaml", pipelines=[p])
    e = Environment()
    e = load_environment(c, env=e)
    p.level = 'debug'
    e = load_environment(c, env=e)
    log = e.get_log(pipeline_name)
    assert log.get_level() == DEBUG


def test_load_environment_with_json_log():
    e = load_test_environment(form='json')
    log = e.get_log(DEFAULT_PIPELINE_NAME)
    assert log.get_format() == 'json'


def test_load_environment_with_unknown_format():
    with raises(ConfigError):
        load_test_environment(form='doesnt_exist')


def test_load_environment_with_multiple_drains():
    pipeline_name = 'test_pipeline'
    p = PipelineConfig(name=pipeline_name, form='simple', level='info')
    p.drains.append(DrainConfig(drain_type='stderr'))
    p.drains.append(DrainConfig(drain_type='file', properties={'name': 'test.log'}))
    c = Config(filepath="test/config/multiple_drains.yaml", pipelines=[p])
    e = Environment()
    e = load_environment(c, env=e)
    drains = e.logs['test_pipeline'].drains
    assert len(drains) == 2
    assert isinstance(drains[0], StderrDrain)
    assert drains[0].name == 'stderr'
    assert isinstance(drains[1], FileDrain)
    assert drains[1].name == 'file:test.log'


def test_load_environment_with_bad_drain():
    with raises(ConfigError):
        pipeline_name = 'test_pipeline'
        p = PipelineConfig(name=pipeline_name, form='simple', level='info')
        p.drains.append(DrainConfig(drain_type='doesnt-exist'))
        c = Config(filepath="test/config/multiple_drains.yaml", pipelines=[p])
        e = Environment()
        load_environment(c, env=e)
