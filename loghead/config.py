"""
The config allows for pre-configured loggers in YAML format.

TODO:
* Add schema
"""
from os.path import basename

import yaml


class PipelineConfig:
    """
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
        self.filepath = other.filepath
        self.filename = other.filename
        self.pipelines = other.pipelines


def load_config(path: str) -> Config:
    """
    Load config file to Config object.
    """
    with open(path, "r") as f:
        conf = yaml.safe_load(f)
        pipelines = parse_pipelines(conf)
        config = Config(path, pipelines)
        return config


def parse_pipeline_config(name, pipeline_data: dict) -> PipelineConfig:
    level = parse_level(pipeline_data)
    formatter = parse_format(pipeline_data)
    p = PipelineConfig(name, level=level, form=formatter)
    return p


def parse_pipelines(conf: dict) -> list[PipelineConfig]:
    ret = list()
    for name, pipeline_data in conf.items():
        p = parse_pipeline_config(name, pipeline_data)
        ret.append(p)
    return ret


def parse_level(pipeline_data: dict) -> str:
    val = pipeline_data.get("level", "info")
    # todo: validate
    return val


def parse_format(pipeline_data: dict) -> str:
    val = pipeline_data.get("format", "simple")
    return val
