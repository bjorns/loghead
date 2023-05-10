"""
Kuvio is a new logging package for Python. Its primary goals are beauty and developer Joy.
"""
from .config import load_config
from .factory import load_environment
from .root import debug, info, notice, warning, error


def init(path: str):
    c = load_config(path)
    print(c)
    load_environment(c)
