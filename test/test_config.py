from pytest import raises

from loghead.config import load_config, ConfigError, Location, parse_location


def test_config_error():
    err = ConfigError("hello world")
    assert str(err) == "hello world"
    assert repr(err) == "hello world"
    err = ConfigError("hello world", loc=Location("foobar.yaml", line_start=17, line_end=19))
    assert str(err) == "foobar.yaml:17..19: hello world"
    assert repr(err) == "foobar.yaml:17..19: hello world"


def test_load_file():
    config = load_config('test/config/debug_log.yaml')
    assert config.filepath == 'test/config/debug_log.yaml'
    assert config.filename == 'debug_log.yaml'
    assert len(config.pipelines) == 1
    pipeline_config = config.pipelines[0]
    assert pipeline_config.name == 'my_log'
    assert pipeline_config.level == 'debug'


def test_str_representation():
    config = load_config('test/config/debug_log.yaml')
    assert str(config) == "Config<test/config/debug_log.yaml>"
    pipeline_config = config.pipelines[0]
    assert str(pipeline_config) == "PipelineConfig<my_log>"


def test_update_config():
    config = load_config('test/config/debug_log.yaml')
    second_config = load_config('test/config/info_log.yaml')
    config.update(second_config)
    assert config.filepath == 'test/config/info_log.yaml'
    assert config.filename == 'info_log.yaml'
    assert len(config.pipelines) == 1
    pipeline_config = config.pipelines[0]
    assert pipeline_config.name == 'my_log'
    assert pipeline_config.level == 'info'


def test_bad_level_config_error():
    with raises(ConfigError) as e:
        load_config('test/config/bad_level.yaml')
    assert str(e.value) == "bad_level.yaml:3..3: Level does_not_exist does not exist"


def test_int_level_config_error():
    with raises(ConfigError) as e:
        load_config('test/config/integer_level.yaml')
    assert str(e.value) == "integer_level.yaml:3..3: Expected level: property to be string, got int(3)"


def test_int_format_config_error():
    with raises(ConfigError) as e:
        load_config('test/config/integer_format.yaml')
    assert str(e.value) == "integer_format.yaml:3..4: Expected format property to be string, got int(3)"


def test_no_location():
    loc = parse_location(dict())
    assert loc == Location('unknown', line_start=-1, line_end=-1)
