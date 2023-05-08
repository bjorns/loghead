"""
Root logging
"""
from .log import LogPipeline

_root_logger = LogPipeline()

def info(msg: str):
	_root_logger.info(msg)
