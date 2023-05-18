"""
Root log convenience functions
"""
from .environment import get_root_log


def debug(msg: str):
    """ Log debug event on root logger. """
    get_root_log().debug(msg)


def info(msg: str):
    """ Log info event on root logger. """
    get_root_log().info(msg)


def notice(msg: str):
    """ Log notice event on root logger. """
    get_root_log().notice(msg)


def warning(msg: str):
    """ Log warning event on root logger. """
    get_root_log().warning(msg)


def error(msg: str):
    """ Log error event on root logger. """
    get_root_log().error(msg)
