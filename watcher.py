from multiprocessing import Event, Process, Queue
from enum import Enum
import time
from twitch_handler import TwitchHandler
from browser_handler import BrowserHandler
from cookie_handler import CookieHandler
from preferences_handler import PreferencesHandler, ChannelErrorState
from data_container import WatcherInputDataContainer, WatcherOutputDataContainer


class WatcherRoutineState(Enum):
    STARTING = 0
    CHECKING_LOGIN_STATUS = 1
    LOOKING_FOR_CHANNEL = 2
    WATCHING = 3
    IDLING = 4
    QUITING = 5


class WatcherErrorState(Enum):
    NOT_SET = "Watcher data container not set"
    ALREADY_RUNNING = "Watcher is already running"
    ALREADY_STOPPED = "Watcher is already stopped"
    FAILED_TO_START = "Watcher failed to start"
    FAILED_TO_OPEN_BROWSER = "Failed to open browser"
    FAILED_TO_OPEN_LOGIN_PAGE = "Failed to open Twitch login page"
    FAILED_TO_LOGIN = "Failed to login to Twitch"
    FAILED_TO_UNMUTE = "Failed to unmute stream"
    FAILED_TO_GET_STREAM_GAME = "Failed to get stream game"
    FAILED_TO_GET_STREAM_TITLE = "Failed to get stream title"
    FAILED_TO_GET_VIEWERS = "Failed to get stream viewers"
    FAILED_TO_GET_POINTS = "Failed to get stream points"
    FAILED_TO_CLAIM_POINTS = "Failed to claim stream points"
    FAILED_TO_CLAIM_DROP = "Failed to claim stream drop"
    FAILED_TO_GET_LATEST_DROP_NAME = "Failed to get latest drop title"
    FAILED_TO_GET_LATEST_DROP_GAME = "Failed to get latest drop game"
    FAILED_TO_GET_LATEST_DROP_DATE = "Failed to get latest drop date"


class Watcher:
    def __init__(self, input_data_container: WatcherInputDataContainer):
        self.input_data_container = input_data_container
        self._process = None
        self._stop_event = None
        self._running = False
        self._queue = None

    def start(self) -> WatcherErrorState:
        if self._running:
            return WatcherErrorState.ALREADY_RUNNING
        if self.input_data_container is None:
            return WatcherErrorState.NOT_SET
        self._queue = Queue()
        self._running = True
        self._stop_event = Event()
        self._process = Process(target=self._routine,
                                args=(self.input_data_container,
                                      self._stop_event,))
        self._process.start()

    def stop(self) -> WatcherErrorState:
        if not self._running:
            return WatcherErrorState.ALREADY_RUNNING
        self._stop_event.set()
        self._process.join()
        self._process = None
        self._running = False

    def get_output_data(self) -> WatcherOutputDataContainer:
        if self._queue is not None:
            try:
                return self._queue.get()
            except self._queue.Empty:
                pass

    def _routine(self, input_data_container: WatcherInputDataContainer, stop_event: Event):
        browser_handler = BrowserHandler()
        browser_handler.browser_import_cookies(input_data_container.channels, input_data_container.cookie_data)
        twitch_handler = TwitchHandler(browser_handler=browser_handler)
        preferences_handler = PreferencesHandler()
        browser_handler.browser_start()
        output_data_container = WatcherOutputDataContainer()
        while not stop_event.is_set():
            output_data_container.routine_state = WatcherRoutineState.STARTING
            self._queue.put(output_data_container)
            time.sleep(1)
