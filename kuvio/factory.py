"""

"""
from .config import Config, PipelineConfig
from .level import Level, get_level
from .log import Log, LogPipeline

_logs = dict()


def get_log(name: str) -> Log:
    """
    """
    log = _logs.get(name, None)
    if log is None:
        # todo: find closest logger
        log = LogPipeline()
    return log


def load_environment(config: Config):
    """
    Create or update the current environment from the confif
    """
    global _logs
    for pipeline_config in config.pipelines:
        new_log = load_pipeline(pipeline_config)
        print(new_log)
        if new_log.name in _logs:
            log = _logs[new_log.name]
            log.update(new_log)
        else:
            _logs[new_log.name] = new_log


def load_pipeline(pipeline_config: PipelineConfig) -> LogPipeline:
    """
    Create a log pipeline from the config.
    """
    level = get_level(pipeline_config.level)
    return LogPipeline(name=pipeline_config.name, level=level)
