class LogheadError(Exception):
    """
    System baseclass
    """
    pass


class UserError(LogheadError):
    """
    The user of the package performed an incorrect or
    not allowed operation.
    """
    pass


class BaseclassError(UserError):
    """
    The user called an abstract baseclass which should not
    be called directly
    """
    pass


class UnimplementedError(LogheadError):
    """
    This functionality is not implemented yet but the user is not
    wrong in calling it.
    """
    pass
