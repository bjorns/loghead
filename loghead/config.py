"""
The config allows for pre-configured loggers in YAML format.

TODO:
* Add schema
"""
from dataclasses import dataclass
from os.path import basename

from yaml import load, SafeLoader

from .error import UserError, InternalError
from .level import LEVEL_BY_NAME


@dataclass
class Location:
    """
    A collection of data for error reporting on where config originates.
    """
    filename: str
    line_start: int
    line_end: int


class ConfigError(UserError):
    """
    The system tried to load a config that it does not recognize
    """

    def __init__(self, message: str, loc: Location = None):
        super().__init__(message)
        self.message = message
        self.loc = loc

    def __str__(self):
        return repr(self)

    def __repr__(self):
        if self.loc:
            return f"{self.loc.filename}:{self.loc.line_start}..{self.loc.line_end}: {self.message}"
        return self.message


class PipelineConfig:
    """
    Config for a single pipeline description in the larger Config object.
    """

    def __init__(self, name: str, level: str, form: str, loc: Location = None):
        self.name = name
        self.level = level
        self.format = form
        self.loc = loc

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


class LocationMetadataLoader(SafeLoader):
    """
    Loader class to counts line numbers for improved error reporting on bad
    config
    """

    def __init__(self, filename: str, stream):
        super().__init__(stream)
        self.filename = filename

    def construct_mapping(self, node, deep=False):
        mapping = super().construct_mapping(node, deep=deep)
        # Add 1 so line numbering starts at 1
        mapping['__loc__'] = Location(filename=self.filename, line_start=node.start_mark.line + 1,
                                      line_end=node.end_mark.line)
        return mapping


def load_config(path: str) -> Config:
    """
    Load config file to Config object.
    """

    def _loader(stream):
        """
        Internal loader function to bind the filename parameter
        """
        return LocationMetadataLoader(basename(path), stream)

    with open(path, "r", encoding='utf-8') as f:
        conf_data = load(f, Loader=_loader)
        pipelines = parse_pipelines(conf_data)
        config = Config(path, pipelines)
        return config


def parse_pipelines(conf_data: dict) -> list[PipelineConfig]:
    """
    Parse the pipelines defined in the config data.
    """
    ret = []
    for pipeline_name, pipeline_data in conf_data.items():
        if pipeline_name.startswith('__') and pipeline_name.endswith('__'):
            # The config object will have a __line__ attribute which needs to be ignored.
            continue
        pipeline_config = parse_pipeline_config(pipeline_name, pipeline_data)
        ret.append(pipeline_config)
    return ret


def parse_pipeline_config(pipeline_name: str, pipeline_data: dict) -> PipelineConfig:
    """
    Generate a PipelineConfig object from the raw data read from the Yaml/Json
    file.

    :param pipeline_name: The name of the pipeline
    :param pipeline_data: the data read from Yaml.
    """
    level = parse_level(pipeline_data)
    formatter = parse_format(pipeline_data)
    loc = parse_location(pipeline_data)
    return PipelineConfig(pipeline_name, level=level, form=formatter, loc=loc)


def parse_level(pipeline_data: dict) -> str:
    """
    Read the log level configured in the pipeline, defaults to 'info'.
    """
    val = pipeline_data.get("level", "info")
    if not isinstance(val, str):
        raise ConfigError(f"Expected level: property to be string, got {type(val).__name__}({val})",
                          loc=_safe_loc(pipeline_data))
    if val not in LEVEL_BY_NAME:
        raise ConfigError(f"Level {val} does not exist",
                          loc=_safe_loc(pipeline_data))
    return val


def parse_format(pipeline_data: dict) -> str:
    """
    Read the format configured in the pipeline config. Default to 'simple'.
    """
    val = pipeline_data.get("format", "simple")
    if not isinstance(val, str):
        raise ConfigError(f"Expected format property to be string, got {type(val).__name__}({val})",
                          loc=_safe_loc(pipeline_data))
    return val


def parse_location(data: dict) -> Location:
    """
    Each parsed node of the tree will have a '__line__' property thanks to
    SafeLineLoader.
    """
    location = data.get('__loc__')
    if location is None:
        return Location(filename='unknown', line_start=-1, line_end=-1)
    return location


def _safe_loc(data: dict):
    return data.get('__loc__')
