from kuvio.config import load_config


def test_load_file():
    config = load_config('test/config/single_pipeline.yaml')
    assert config.filepath == 'test/config/single_pipeline.yaml'
    assert config.filename == 'single_pipeline.yaml'
    assert len(config.pipelines) == 1
    pipeline_config = config.pipelines[0]
    assert pipeline_config.name == 'my_log'
    assert pipeline_config.level == 'debug'


def test_str_representation():
    config = load_config('test/config/single_pipeline.yaml')
    assert str(config) == "Config<test/config/single_pipeline.yaml>"
    pipeline_config = config.pipelines[0]
    assert str(pipeline_config) == "PipelineConfig<my_log>"


def test_update_config():

    config = load_config('test/config/single_pipeline.yaml')
    second_config = load_config('test/config/single_pipeline_updated.yaml')
    config.update(second_config)
    assert config.filepath == 'test/config/single_pipeline_updated.yaml'
    assert config.filename == 'single_pipeline_updated.yaml'
    assert len(config.pipelines) == 1
    pipeline_config = config.pipelines[0]
    assert pipeline_config.name == 'my_log'
    assert pipeline_config.level == 'info'
