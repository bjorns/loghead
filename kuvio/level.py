"""
We redefine the log levels to line up with logging package just in case.
We add one extra level NOTICE which is for important but non-error related
messages.
"""

DEBUG = 10
INFO = 20
NOTICE = 25
WARNING = 30
ERROR = 40
FATAL = 50
DISABLED = 100
