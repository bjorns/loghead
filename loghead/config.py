"""
The config allows for pre-configured loggers in YAML format.

TODO:
* Add schema
"""
from os.path import basename

from yaml import load, SafeLoader

from .error import InternalError, BadConfigError, ERROR_LINE_INTERVAL
from .level import LEVEL_BY_NAME


class PipelineConfig:
    """
    Config for a single pipeline description in the larger Config object.
    """

    def __init__(self, name: str, level: str, form: str, line_num: int):
        self.name = name
        self.level = level
        self.format = form
        self.line_num = line_num

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


class SafeLineLoader(SafeLoader):
    """
    Loader class to counts line numbers for improved error reporting on bad
    config
    """

    def construct_mapping(self, node, deep=False):
        mapping = super().construct_mapping(node, deep=deep)
        # Add 1 so line numbering starts at 1
        mapping['__line__'] = (node.start_mark.line + 1, node.end_mark.line)
        return mapping


def load_config(path: str) -> Config:
    """
    Load config file to Config object.
    """
    with open(path, "r", encoding='utf-8') as f:
        conf_data = load(f, Loader=SafeLineLoader)
        pipelines = parse_pipelines(conf_data)
        config = Config(path, pipelines)
        return config


def parse_pipelines(conf_data: dict) -> list[PipelineConfig]:
    """
    Parse the pipelines defined in the config data.
    """
    ret = []
    for name, pipeline_data in conf_data.items():
        if name.startswith('__') and name.endswith('__'):
            continue
        pipeline_config = parse_pipeline_config(name, pipeline_data)
        ret.append(pipeline_config)
    return ret


def parse_pipeline_config(name: str, pipeline_data: dict) -> PipelineConfig:
    """
    Generate a PipelineConfig object from the raw data read from the Yaml/Json
    file.

    :param name: The name of the pipeline
    :param pipeline_data: the data read from Yaml.
    """
    level = parse_level(pipeline_data)
    formatter = parse_format(pipeline_data)
    line_num = parse_line_number(pipeline_data)
    return PipelineConfig(name, level=level, form=formatter, line_num=line_num)


def parse_level(pipeline_data: dict) -> str:
    """
    Read the log level configured in the pipeline, defaults to 'info'.
    """
    val = pipeline_data.get("level", "info")
    if not isinstance(val, str):
        raise InternalError(f"Expected level: property to be string, got {type(val)}({val})")
    if val not in LEVEL_BY_NAME:
        raise BadConfigError(f"Level {val} does not exist", line_num=pipeline_data.get('__line__', -1))
    return val


def parse_format(pipeline_data: dict) -> str:
    """
    Read the format configured in the pipeline config. Default to 'simple'.
    """
    val = pipeline_data.get("format", "simple")
    if not isinstance(val, str):
        raise InternalError(f"Expected format: property to be string, got {type(val)}({val})")
    return val


def parse_line_number(data: dict) -> tuple:
    """
    Each parsed node of the tree will have a '__line__' property thanks to
    SafeLineLoader.
    """
    start, end = data.get('__line__', ERROR_LINE_INTERVAL)
    if not isinstance(start, int) or not isinstance(end, int):
        raise InternalError(f"No line number property was located in data node: {data}")
    return start, end
