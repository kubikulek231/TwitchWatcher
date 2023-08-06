import sys
import time

from handler.cookie_handler import CookieHandler
from handler.preferences_handler import PreferencesHandler, ChannelErrorState
from ui.ui_handler_main import UIHandlerMain, UICleaner
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
        print("    Press Ctrl+C to cancel")
        print("")
        try:
            for i in range(10, 0, -1):
                print(f"   {i}")
                time.sleep(1)
            print("")
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

    ui_handler = UIHandlerMain(are_cookies_loaded, are_preferences_loaded,
                               preferences_handler.options, preferences_handler.channels)
    while True:
        option = ui_handler.run()
        ui_handler.print_ui = True
        ui_handler.clear_console = True
        match option:
            case 1:
                # run watcher
                if preferences_handler.channels and cookie_handler.cookie_data:
                    ui_handler.show_logo()
                    input_data_container = WatcherInputDataContainer(preferences_handler.channels,
                                                                     cookie_handler.cookie_data)
                    UIHandlerRun(input_data_container).run()
                else:
                    print("\n - No channels or cookies are set")
                    print("    Please set channels and cookies first\n")
                    ui_handler.print_ui = False
                    ui_handler.clear_console = False
            case 2:
                # add new channel
                UICleaner.clear_console()
                ui_handler.show_logo()
                print(" - Add new channel menu")
                ui_handler.print_channel_bar(preferences_handler.channels)
                while True:
                    channel_to_add = UIHandlerSettings.input_channel()
                    if channel_to_add is None:
                        break
                    print("")
                    print(" Channel added successfully." if preferences_handler.channel_add(channel_to_add) is None
                          else " Channel already exists.")
                ui_handler.update(preferences_handler.options, preferences_handler.channels)
            case 3:
                # remove channel
                UICleaner.clear_console()
                ui_handler.show_logo()
                print(" - Remove a channel menu")
                ui_handler.print_channel_bar(preferences_handler.channels)
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
                UICleaner.clear_console()
                ui_handler.show_logo()
                print(" - Move channel up menu")
                ui_handler.print_channel_bar(preferences_handler.channels)
                while True:
                    channel_to_move = UIHandlerSettings.input_channel()
                    if channel_to_move is None:
                        break
                    move_result = preferences_handler.channel_move_up(channel_to_move)
                    print("")
                    if move_result is None:
                        print(" Channel moved up successfully.")
                        ui_handler.print_channel_bar(preferences_handler.channels)
                    if move_result == ChannelErrorState.CHANNEL_ALREADY_ON_TOP:
                        print(" Channel is already on top.")
                    if move_result == ChannelErrorState.CHANNEL_DOES_NOT_EXIST:
                        print(" Channel does not exist.")
            case 5:
                # move channel down
                UICleaner.clear_console()
                ui_handler.show_logo()
                print(" - Move channel down menu")
                ui_handler.print_channel_bar(preferences_handler.channels)
                while True:
                    channel_to_move = UIHandlerSettings.input_channel()
                    if channel_to_move is None:
                        break
                    move_result = preferences_handler.channel_move_down(channel_to_move)
                    print("")
                    if move_result is None:
                        print(" Channel moved down successfully.")
                        ui_handler.print_channel_bar(preferences_handler.channels)
                    if move_result == ChannelErrorState.CHANNEL_ALREADY_ON_BOTTOM:
                        print(" Channel is already on bottom.")
                    if move_result == ChannelErrorState.CHANNEL_DOES_NOT_EXIST:
                        print(" Channel does not exist.")
                ui_handler.print_ui = True
            case 6:
                # toggle run on start
                UICleaner.clear_console()
                preferences_handler.option_set("app_run_on_start",
                                               not preferences_handler.options.get("app_run_on_start"))
            case 7:
                # toggle save on exit
                UICleaner.clear_console()
                preferences_handler.option_set("app_save_on_exit",
                                               not preferences_handler.options.get("app_save_on_exit"))
            case 8:
                # save preferences and cookies to file
                if preferences_handler.save_to_file() is None:
                    print(" Preferences saved successfully")
                else:
                    print(" Error saving preferences")
                if cookie_handler.save_to_file() is None:
                    print(" Cookies saved successfully")
                else:
                    print(" Error saving cookies")
                print("")
                ui_handler.print_ui = False
                ui_handler.clear_console = False
            case 9:
                # load cookies from clipboard
                UICleaner.clear_console()
                ui_handler.show_logo()
                print(" - Load cookies from clipboard menu")
                while True:
                    cookie_file = UIHandlerSettings.input_cookie_json_file()
                    if cookie_file is None:
                        break
                    print(" Cookies loaded successfully." if cookie_handler.load_from_string(cookie_file) is None
                          else " Invalid cookie JSON. Try again.")
            case 0:
                # exit
                UICleaner.clear_console()
                ui_handler.show_logo()
                if preferences_handler.options.get("app_save_on_exit"):
                    if preferences_handler.save_to_file() is None:
                        print(" Preferences saved successfully")
                    if cookie_handler.save_to_file() is None:
                        print(" Cookies saved successfully")
                print(" Exiting\n")
                sys.exit(0)
            case _:
                print(" Invalid option. Try again.")
