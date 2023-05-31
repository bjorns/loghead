"""
Convert config objects to log pipelines
"""
from .config import Config, PipelineConfig, ConfigError, DrainConfig
from .drain import Drain, StderrDrain, FileDrain
from .environment import Environment, get_global_env
from .filter import LevelFilter
from .format import Format, SimpleFormat, SimpleJsonFormat
from .internal import debuglog
from .level import get_level
from .log import LogPipeline


def load_environment(config: Config, env: Environment = None) -> Environment:
    """
    Create or update the current environment from the confif

    :param config: The Config object to load into env
    :param env: The environment to load, if None, default to global env.
    """
    if env is None:
        env = get_global_env()
    for pipeline_config in config.pipelines:
        new_log = load_pipeline(pipeline_config)
        debuglog("loaded log: %s", new_log)
        if env.has_log(new_log.name):
            log = env.get_log(new_log.name)
            log.update(new_log)
        else:
            env.set_log(new_log.name, new_log)
    debuglog("")
    return env


def load_pipeline(pipeline_config: PipelineConfig) -> LogPipeline:
    """
    Create a log pipeline from the config.
    """
    level_filter = load_level(pipeline_config.level)
    form = load_format(pipeline_config.format)
    drains = load_drains(pipeline_config.drains)
    return LogPipeline(pipeline_config.name, level_filter, form, *drains)


def load_level(level_name: str) -> LevelFilter:
    """
    Convert the level string from config to a LevelFilter object that allows
    only higherleveled log events.
    """
    level = get_level(level_name)
    return LevelFilter(level)


def load_format(format_name: str) -> Format:
    """
    Parse the format setting from config and create a foramtter object
    for the final log pipeline.
    """
    if format_name == 'simple':
        return SimpleFormat()
    if format_name == 'json':
        return SimpleJsonFormat()
    raise ConfigError(f"Unknown format requested: {format_name}")


def load_drains(drain_configs: list[DrainConfig]) -> list[Drain]:
    """
    Generate all drains required for the pipeline. A Pipeline can have multiple drains such as
    a file and the standard error stream.
    """
    return list(load_drain(drain_config) for drain_config in drain_configs)


def load_drain(drain_config: DrainConfig) -> Drain:
    """
    Create Drain component from the provided config
    """
    if drain_config.type == 'stderr':
        return StderrDrain()
    if drain_config.type == 'file':
        return FileDrain(filepath=drain_config.properties['name'])
    else:
        raise ConfigError(f"Unknown drain config {drain_config}", drain_config.loc)
