from pytest import raises

from loghead.config import load_config, ConfigError, Location, parse_location, DrainConfig


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


def test_parse_file_drain_log():
    config = load_config('test/config/file_drain.yaml')
    assert len(config.pipelines) == 1
    pipeline_config = config.pipelines[0]
    assert len(pipeline_config.drains) == 1
    drain = pipeline_config.drains[0]
    assert drain.type == 'file'
    assert drain.loc == Location('file_drain.yaml', line_start=5, line_end=4)


def test_parse_multiple_drains_log():
    config = load_config('test/config/multiple_drains.yaml')
    assert len(config.pipelines) == 1
    pipeline_config = config.pipelines[0]
    assert len(pipeline_config.drains) == 2
    file_drain = pipeline_config.drains[0]
    assert file_drain.type == 'file'
    assert file_drain.loc == Location('multiple_drains.yaml', line_start=5, line_end=5)
    stderr_drain = pipeline_config.drains[1]
    assert stderr_drain.type == 'stderr'
    assert stderr_drain.loc is None  # why is this?


def test_drain_with_multiple_props_raises():
    with raises(ConfigError) as e:
        load_config('test/config/drain_with_multi_prop.yaml')
    expected_item = {
        'file': {
            'name': 'app.log'
        },
        'something_else': 'foobar'
    }
    assert str(e.value) == f"Write config should have a single item, found 2: {expected_item}"


def test_drain_with_list():
    with raises(ConfigError) as e:
        load_config('test/config/int_drain.yaml')
    assert str(e.value) == "Unexpected write config 4711, expected str or dict"


def test_drain_config_repr():
    assert repr(DrainConfig(drain_type='stderr')) == "DrainConfig<stderr>"
   