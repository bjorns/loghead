"""

"""
from .config import Config, PipelineConfig
from .error import UserError
from .filter import LevelFilter
from .format import Format, SimpleFormat, SimpleJsonFormat
from .internal import debuglog
from .level import get_level
from .log import Log, LogPipeline
from .root import root_log

_logs = {
    'root': root_log
}


def get_log(name: str) -> Log:
    """
    """
    log = _logs.get(name, None)
    if log is None:
        # todo: find closest logger
        log = LogPipeline(name)
    return log


def load_environment(config: Config):
    """
    Create or update the current environment from the confif
    """
    global _logs
    for pipeline_config in config.pipelines:
        new_log = load_pipeline(pipeline_config)
        debuglog("loaded log: %s", new_log)
        if new_log.name in _logs:
            log = _logs[new_log.name]
            log.update(new_log)
        else:
            _logs[new_log.name] = new_log
    debuglog("")


def load_level(level_name: str) -> LevelFilter:
    level = get_level(level_name)
    return LevelFilter(level)


def load_format(format_name: str) -> Format:
    if format_name == 'simple':
        return SimpleFormat()
    elif format_name == 'json':
        return SimpleJsonFormat()
    else:
        raise UserError(f"Unknown format requested: {format_name}")


def load_pipeline(pipeline_config: PipelineConfig) -> LogPipeline:
    """
    Create a log pipeline from the config.
    """
    level_filter = load_level(pipeline_config.level)
    form = load_format(pipeline_config.format)
    return LogPipeline(pipeline_config.name, level_filter, form)
