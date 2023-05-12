"""
Internal logging that does it simpler and does not create dependency loops in the code.
"""
from sys import stderr

DEBUG_ENABLED = True


def debuglog(msg: str, *argv):
    """
    Write message to stderr
    """
    if not DEBUG_ENABLED:
        return
    formatted = msg % tuple(argv)
    stderr.write(f"internal: {formatted}\n")
