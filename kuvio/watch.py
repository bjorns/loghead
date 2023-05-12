from watchdog.events import FileSystemEventHandler, LoggingEventHandler, RegexMatchingEventHandler
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver

from .config import Config, load_config
from .factory import load_environment
from .debug import debuglog


class ConfigEventHandler(FileSystemEventHandler):
    """
    The config event handler implements the Watchdog
    file event handler interface in order to get
    file save events from the source config file
    """

    def __init__(self, filepath: str):
        super(ConfigEventHandler, self).__init__()

    def on_modified(self, event):
        """
        File was modified
        """
        super(ConfigEventHandler, self).on_modified(event)
        debuglog("file modified event: %s", event.src_path)
        c = load_config(event.src_path)
        load_environment(c)

    def on_created(self, event):
        """
        For whatever reason a file save often shows up as a file created event.
        """
        super(ConfigEventHandler, self).on_created(event)
        debuglog("file created event: %s", event.src_path)
        c = load_config(event.src_path)
        load_environment(c)


class ConfigFileWatchdog:
    def __init__(self, config: Config, observer: Observer = None, event_handler=None):
        event_handler = event_handler or ConfigEventHandler(config)
        self.observer = observer or PollingObserver()
        self.observer.schedule(event_handler, config.filepath)
        self.filepath = config.filepath

    def sit_booboo(self):
        debuglog("starting filewatcher %s", self.filepath)
        self.observer.start()
