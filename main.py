from watcher import Watcher
from watcher_data_container import WatcherInputDataContainer
from cookie_handler import CookieHandler
from preferences_handler import PreferencesHandler
import time

if __name__ == '__main__':
    cookie_handler = CookieHandler()
    cookie_handler.load_from_file()
    preferences_handler = PreferencesHandler()
    preferences_handler.load_from_file()
    input_data_container = WatcherInputDataContainer(preferences_handler.channels, cookie_handler.cookie_data)
    watcher = Watcher(input_data_container)
    watcher.start()
    while True:
        print(watcher.get_output_data().__dict__)
        time.sleep(1)


