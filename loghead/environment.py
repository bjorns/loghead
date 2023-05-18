from .log import Log, LogPipeline


class Environment:
    """
    Environment captures the full set of logs in the system. A user can request
    a named log and the system will return the best matching logger. If not
    logger matches, the root log will be returned.
    """

    def __init__(self):
        self.logs = dict[str, Log]()
        self.logs['root'] = LogPipeline(name='root')

    def has_log(self, name: str) -> bool:
        return name in self.logs

    def get_log(self, name: str) -> Log:
        """
        Todo:
        Map closest available log. E.g. if requesting package.module and
        package exist, return it. If not, return root logger.
        """
        ret = self.logs.get(name)
        if ret is None:
            ret = self.get_root_log()
        return ret

    def set_log(self, name: str, log: Log):
        self.logs[name] = log

    def get_root_log(self):
        return self.get_log('root')


"""
_env is the global default environment. A user can create their own env and work
directly with it but we provide package root methods to work directly with the
default env for convenience.
"""
_env = Environment()


def get_root_log():
    return _env.get_root_log()


def get_log(name: str) -> Log:
    """
    """
    return _env.get_log(name)


def set_log(name: str, log: Log):
    _env.set_log(name, log)


def has_log(name: str) -> bool:
    return _env.has_log(name)


def get_global_env():
    return _env
