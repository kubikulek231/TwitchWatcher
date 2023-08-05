import sys
import time

from handler.cookie_handler import CookieHandler
from handler.preferences_handler import PreferencesHandler, ChannelErrorState
from ui.ui_handler_main import UIHandlerMain
from ui.ui_handler_run import UIHandlerRun
from ui.ui_handler_settings import UIHandlerSettings
from watcher.watcher_data_container import WatcherInputDataContainer

if __name__ == "__main__":
    cookie_handler = CookieHandler()
    are_cookies_loaded = cookie_handler.load_from_file() is None
    preferences_handler = PreferencesHandler()
    are_preferences_loaded = preferences_handler.load_from_file() is None

    if preferences_handler.options.get("app_run_on_start"):
        # 10 sec countdown
        skipped = False
        UIHandlerMain.show_logo()
        print(" - Starting in 10 seconds")
        print("   Press Ctrl+C to cancel")
        print("")
        try:
            for i in range(10, 0, -1):
                print(f"   {i}")
                time.sleep(1)
        except KeyboardInterrupt:
            print("")
            print(" - Canceled")
            skipped = True
        # run watcher
        if not skipped:
            UIHandlerMain.show_logo()
            input_data_container = WatcherInputDataContainer(preferences_handler.channels,
                                                             cookie_handler.cookie_data)
            UIHandlerRun(input_data_container).run()

    while True:
        option = UIHandlerMain(are_cookies_loaded, are_preferences_loaded, cookie_handler.cookie_data,
                               preferences_handler.options, preferences_handler.channels).run()
        match option:
            case 1:
                # run watcher
                UIHandlerMain.show_logo()
                input_data_container = WatcherInputDataContainer(preferences_handler.channels,
                                                                 cookie_handler.cookie_data)
                UIHandlerRun(input_data_container).run()
            case 2:
                # add new channel
                UIHandlerMain.show_logo()
                print(" - Add new channel menu")
                UIHandlerMain.print_channel_bar(preferences_handler.channels)
                while True:
                    channel_to_add = UIHandlerSettings.input_channel()
                    if channel_to_add is None:
                        break
                    print("")
                    print(" Channel added successfully." if preferences_handler.channel_add(channel_to_add) is None
                          else " Channel already exists.")
            case 3:
                # remove channel
                UIHandlerMain.show_logo()
                print(" - Remove a channel menu")
                UIHandlerMain.print_channel_bar(preferences_handler.channels)
                while True:
                    channel_to_remove = UIHandlerSettings.input_channel()
                    if channel_to_remove is None:
                        break
                    print("")
                    print(" Channel removed successfully."
                          if preferences_handler.channel_remove(channel_to_remove)
                          is None else " Channel does not exist.")
            case 4:
                # move channel up
                UIHandlerMain.show_logo()
                print(" - Move channel up menu")
                UIHandlerMain.print_channel_bar(preferences_handler.channels)
                while True:
                    channel_to_move = UIHandlerSettings.input_channel()
                    if channel_to_move is None:
                        break
                    move_result = preferences_handler.channel_move_up(channel_to_move)
                    print("")
                    if move_result is None:
                        print(" Channel moved up successfully.")
                        UIHandlerMain.print_channel_bar(preferences_handler.channels)
                    if move_result == ChannelErrorState.CHANNEL_ALREADY_ON_TOP:
                        print(" Channel is already on top.")
                    if move_result == ChannelErrorState.CHANNEL_DOES_NOT_EXIST:
                        print(" Channel does not exist.")
            case 5:
                # move channel down
                UIHandlerMain.show_logo()
                print(" - Move channel down menu")
                UIHandlerMain.print_channel_bar(preferences_handler.channels)
                while True:
                    channel_to_move = UIHandlerSettings.input_channel()
                    if channel_to_move is None:
                        break
                    move_result = preferences_handler.channel_move_down(channel_to_move)
                    print("")
                    if move_result is None:
                        print(" Channel moved down successfully.")
                        UIHandlerMain.print_channel_bar(preferences_handler.channels)
                    if move_result == ChannelErrorState.CHANNEL_ALREADY_ON_BOTTOM:
                        print(" Channel is already on bottom.")
                    if move_result == ChannelErrorState.CHANNEL_DOES_NOT_EXIST:
                        print(" Channel does not exist.")
            case 6:
                # toggle run on start
                preferences_handler.option_set("app_run_on_start",
                                               not preferences_handler.options.get("app_run_on_start"))
            case 7:
                # toggle save on exit
                preferences_handler.option_set("app_save_on_exit",
                                               not preferences_handler.options.get("app_save_on_exit"))
            case 8:
                # save preferences and cookies to file
                UIHandlerMain.show_logo()
                if preferences_handler.save_to_file() is None:
                    print(" Preferences saved successfully")
                if cookie_handler.save_to_file() is None:
                    print(" Cookies saved successfully")
            case 9:
                # load cookies from clipboard
                UIHandlerMain.show_logo()
                print(" - Load cookies from clipboard menu")
                while True:
                    cookie_file = UIHandlerSettings.input_cookie_json_file()
                    if cookie_file is None:
                        break
                    print(" Cookies loaded successfully." if cookie_handler.load_from_string(cookie_file) is None
                          else " Invalid cookie JSON. Try again.")
            case 0:
                # exit
                UIHandlerMain.show_logo()
                if preferences_handler.options.get("app_save_on_exit"):
                    if preferences_handler.save_to_file() is None:
                        print(" Preferences saved successfully")
                    if cookie_handler.save_to_file() is None:
                        print(" Cookies saved successfully")
                print(" Exiting\n")
                sys.exit(0)
            case _:
                print(" Invalid option. Try again.")
