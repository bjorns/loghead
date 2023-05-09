"""
The config allows for pre-configured loggers in YAML format.

TODO:
* Add schema
"""
import yaml


class PipelineConfig:
    def __init__(self, name: str, level: str):
        self.name = name
        self.level = level


class Config:
    """
    Data type representing the standard logging config file
    """

    def __init__(self, pipelines: list):
        self.pipelines = pipelines


def load_config(path: str) -> Config:
    """
    Load config file to Config object.
    """
    with open(path, "r") as f:
        conf = yaml.safe_load(f)
        pipelines = parse_pipelines(conf)
        return Config(pipelines)


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
