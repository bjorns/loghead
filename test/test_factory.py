from pytest import raises

from kuvio.config import Config, PipelineConfig
from kuvio.environment import Environment
from kuvio.error import BadConfigError
from kuvio.factory import load_environment
from kuvio.format import SimpleFormat, SimpleJsonFormat
from kuvio.level import DEBUG, INFO

DEFAULT_PIPELINE_NAME = 'test_pipeline'


def load_test_environment(pipeline_name=DEFAULT_PIPELINE_NAME, form='simple', level='info',
                          filepath='test/config/single_pipeline.yaml', global_env=False):
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
    assert type(log.get_format()) == SimpleFormat


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
    c = Config(filepath="test/config/single_pipeline.yaml", pipelines=[p])
    e = Environment()
    e = load_environment(c, env=e)
    p.level = 'debug'
    e = load_environment(c, env=e)
    log = e.get_log(pipeline_name)
    assert log.get_level() == DEBUG


def test_load_environment_with_json_log():
    e = load_test_environment(form='json')
    log = e.get_log(DEFAULT_PIPELINE_NAME)
    assert type(log.get_format()) == SimpleJsonFormat


def test_load_environment_with_unknown_format():
    with raises(BadConfigError):
        load_test_environment(form='doesnt_exist')
        