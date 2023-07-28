from watcher import Watcher
from data_container import WatcherInputDataContainer
from cookie_handler import CookieHandler
from preferences_handler import PreferencesHandler
import time

if __name__ == '__main__':
    cookie_handler = CookieHandler()
    cookie_handler.load_from_file()
    preferences_handler = PreferencesHandler()
    preferences_handler.load_from_file()
    watcher_input_data_container = WatcherInputDataContainer(preferences_handler.channels, cookie_handler.cookie_data())
    watcher = Watcher(watcher_input_data_container)
    print(watcher.start())
    time.sleep(2)
    print("state: " + str(watcher.get_output_data().routine_state))
    print(watcher.stop())
    """
    browser_handler = BrowserHandler()
    twitch_handler = TwitchHandler(browser_handler)
    preferences_json_handler = PreferencesHandler()
    preferences_json_handler.channel_add("skill4ltu")
    print(preferences_json_handler.save_to_file())
    print(preferences_json_handler.options)
    print(preferences_json_handler.channels)
    # print(preferences_json_handler.load_from_file())"""
    """print(browser_handler.browser_start())
    print(browser_handler.browser_import_cookies(cookie_json_handler.cookie_data(), "https://www.twitch.tv"))

    print(twitch_handler.twitch_stream_player_open("skill4ltu"))
    print(twitch_handler.twitch_stream_player_unmute())
    print(browser_handler.browser_open_new_tab())
    print(browser_handler.browser_switch_to_tab(1))
    print(browser_handler.browser_close_tab(0))
    input()
    browser_handler.browser_close()"""
