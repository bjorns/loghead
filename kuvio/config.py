"""
The config allows for pre-configured loggers in YAML format.

TODO:
* Add schema
"""
from os.path import basename
import yaml


class Config:
    """
    Data type representing the standard logging config file
    """

    def __init__(self, filepath: str, pipelines: list):
        self.filepath = filepath
        self.filename = basename(filepath)
        self.pipelines = pipelines

    def __repr__(self):
        return f"Config<{self.filepath}>"


class PipelineConfig:
    """
    """
    def __init__(self, name: str, level: str):
        self.name = name
        self.level = level

    def __repr__(self) -> str:
        return f"PipelineConfig<{self.name}>"


def load_config(path: str) -> Config:
    """
    Load config file to Config object.
    """
    with open(path, "r") as f:
        conf = yaml.safe_load(f)
        pipelines = parse_pipelines(conf)
        return Config(path, pipelines)


def parse_pipelines(conf: dict) -> list[PipelineConfig]:
    ret = list()
    for name, pipeline_data in conf.items():
        print(name)
        print(pipeline_data)
        level = parse_level(pipeline_data)
        p = PipelineConfig(name, level)
        ret.append(p)
    return ret


def parse_level(pipeline_data: dict) -> str:
    val = pipeline_data.get("level", "info")
    # todo: validate
    return val
