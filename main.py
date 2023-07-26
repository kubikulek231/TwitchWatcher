from twitch_handler import *
from browser_handler import *
from cookie_handler import *
from preferences_handler import *

if __name__ == '__main__':
    cookie_json_handler = CookieHandler()
    print(cookie_json_handler.load_from_file())
    browser_handler = BrowserHandler()
    twitch_handler = TwitchHandler(browser_handler)
    preferences_json_handler = PreferencesHandler()
    preferences_json_handler.channel_add("skill4ltu")
    print(preferences_json_handler.save_to_file())
    print(preferences_json_handler.options)
    print(preferences_json_handler.channels)
    # print(preferences_json_handler.load_from_file())
    """print(browser_handler.browser_start())
    print(browser_handler.browser_import_cookies(cookie_json_handler.cookie_data(), "https://www.twitch.tv"))

    print(twitch_handler.twitch_stream_player_open("skill4ltu"))
    print(twitch_handler.twitch_stream_player_unmute())
    print(browser_handler.browser_open_new_tab())
    print(browser_handler.browser_switch_to_tab(1))
    print(browser_handler.browser_close_tab(0))
    input()
    browser_handler.browser_close()"""
