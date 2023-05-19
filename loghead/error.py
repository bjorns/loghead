"""
System errors. LogheadErrors are classified as two classes

LogheadError:
  UserError:
    BaseclassError
    BadConfigError
  UnimplementedError
"""
ERROR_LINE_NO = -1
ERROR_LINE_INTERVAL = (ERROR_LINE_NO, ERROR_LINE_NO)

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


class BadConfigError(UserError):
    """
    The system tried to load a config that it does not recognize

    TODO: can we add file line info here?
    """

    def __init__(self, message, line_num: tuple = ERROR_LINE_INTERVAL):
        super().__init__(message, line_num)
        self.message = message
        self.start_line_num = line_num[0]
        self.end_line_num = line_num[1]

    def __str__(self):
        return f"line {self.start_line_num}..{self.end_line_num}: {self.message}"

    def __repr__(self):
        return "foobar"


class InternalError(LogheadError):
    """
    The system innternals had an unexpected error
    """


class UnimplementedError(LogheadError):
    """
    This functionality is not implemented yet but the user is not
    wrong in calling it.
    """
