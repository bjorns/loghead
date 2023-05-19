"""
The config allows for pre-configured loggers in YAML format.

TODO:
* Add schema
"""
from os.path import basename

import yaml


class PipelineConfig:
    """
    Config for a single pipeline description in the larger Config object.
    """

    def __init__(self, name: str, level: str, form: str):
        self.name = name
        self.level = level
        self.format = form

    def __repr__(self) -> str:
        return f"PipelineConfig<{self.name}>"


class Config:
    """
    Data type representing the standard logging config file
    """

    def __init__(self, filepath: str, pipelines: list[PipelineConfig]):
        self.filepath = filepath
        self.filename = basename(filepath)
        self.pipelines = pipelines

    def __repr__(self):
        return f"Config<{self.filepath}>"

    def update(self, other):
        """
        Update the config object by merging the parameter objects properties
        into the subject.
        """
        self.filepath = other.filepath
        self.filename = other.filename
        self.pipelines = other.pipelines


def load_config(path: str) -> Config:
    """
    Load config file to Config object.
    """
    with open(path, "r", encoding='utf-8') as f:
        conf = yaml.safe_load(f)
        pipelines = parse_pipelines(conf)
        config = Config(path, pipelines)
        return config


def parse_pipeline_config(name: str, pipeline_data: dict) -> PipelineConfig:
    """
    Generate a PipelineConfig object from the raw data read from the Yaml/Json
    file.

    :param name: The name of the pipeline
    :param pipeline_data: the data read from Yaml.
    """
    level = parse_level(pipeline_data)
    formatter = parse_format(pipeline_data)
    return PipelineConfig(name, level=level, form=formatter)


def parse_pipelines(conf: dict) -> list[PipelineConfig]:
    """
    Parse the pipelines defined in the config data.
    """
    ret = []
    for name, pipeline_data in conf.items():
        pipeline_config = parse_pipeline_config(name, pipeline_data)
        ret.append(pipeline_config)
    return ret


def parse_level(pipeline_data: dict) -> str:
    """
    Read the log level configured in the pipeline, defaults to 'info'.
    """
    val = pipeline_data.get("level", "info")
    # todo: validate
    return val


def parse_format(pipeline_data: dict) -> str:
    """
    Read the format configured in the pipeline config. Default to 'simple'.
    """
    val = pipeline_data.get("format", "simple")
    return val
