"""
System errors. LogheadErrors are classified as two classes

LogheadError:
  UserError:
    BaseclassError
    ConfigError
  UnimplementedError
"""


class LogheadError(Exception):
    """
    System baseclass
    """


class UserError(LogheadError):
    """
    The user of the package performed an incorrect or
    not allowed operation.
    """


class BaseclassError(UserError):
    """
    The user called an abstract baseclass which should not
    be called directly
    """


class InternalError(LogheadError):
    """
    The system innternals had an unexpected error
    """


class UnimplementedError(LogheadError):
    """
    This functionality is not implemented yet but the user is not
    wrong in calling it.
    """
