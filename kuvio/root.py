"""
Root logging
"""
from .log import LogPipeline
from .factory import _logs


def info(msg: str):
    root_logger = _logs.get("root")
    root_logger.info(msg)
