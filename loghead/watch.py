"""
Monitor the changes of a config and triger a reload when changed.
"""
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver

from .config import Config, load_config
from .error import UserError
from .factory import load_environment
from .internal import debuglog


class ConfigEventHandler(FileSystemEventHandler):
    """
    The config event handler implements the Watchdog
    file event handler interface in order to get
    file save events from the source config file
    """
    def on_modified(self, event):
        """
        File was modified
        """
        try:
            super().on_modified(event)
            debuglog("file modified event: %s", event.src_path)
            config = load_config(event.src_path)
            load_environment(config)
        except UserError as e:
            debuglog("error: %s", e)

    def on_created(self, event):
        """
        For whatever reason a file save often shows up as a file created event.
        """
        try:
            super().on_created(event)
            debuglog("file created event: %s", event.src_path)
            config = load_config(event.src_path)
            load_environment(config)
        except UserError as e:
            debuglog("error: %s", e)


class ConfigFileWatchdog:
    """
    Wraps and configures the observer object.
    """
    def __init__(self, config: Config, observer: Observer = None, event_handler=None):
        event_handler = event_handler or ConfigEventHandler()
        self.observer = observer or PollingObserver()
        self.observer.schedule(event_handler, config.filepath)
        self.filepath = config.filepath

    def sit_booboo(self):
        """
        Start the watchdog thread
        """
        debuglog("starting filewatcher %s", self.filepath)
        self.observer.start()
