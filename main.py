import sys

from ui_handler_main import UIHandlerMain
from ui_handler_run import UIHandlerRun
from cookie_handler import CookieHandler
from preferences_handler import PreferencesHandler
from watcher_data_container import WatcherInputDataContainer


if __name__ == "__main__":
    cookie_handler = CookieHandler()
    are_cookies_loaded = cookie_handler.load_from_file() is None
    preferences_handler = PreferencesHandler()
    are_preferences_loaded = preferences_handler.load_from_file() is None

    while True:
        option = UIHandlerMain(are_cookies_loaded, are_preferences_loaded, cookie_handler.cookie_data,
                               preferences_handler.options, preferences_handler.channels).run()
        match option:
            case 1:
                input_data_container = WatcherInputDataContainer(preferences_handler.channels,
                                                                 cookie_handler.cookie_data)
                UIHandlerRun(input_data_container).run()
            case 2:
                pass
            case 3:
                break
            case 4:
                break
            case 5:
                break
            case 6:
                break
            case 7:
                break
            case _:
                print("Invalid option. Try again.")
    print("Exiting...")
    sys.exit(0)


