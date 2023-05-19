"""
loghead is a new logging package for Python. Its primary goals are beauty and developer Joy.
"""
from .config import load_config
from .factory import load_environment
from .root import debug, info, notice, warning, error
from .watch import ConfigFileWatchdog


def init(path: str):
    """
    Initialize environment

    :param path: File path to yaml config file.
    """
    config = load_config(path)
    load_environment(config)
    booboo = ConfigFileWatchdog(config)
    booboo.sit_booboo()
