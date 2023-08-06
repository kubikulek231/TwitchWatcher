import sys
import time

from handler.cookie_handler import CookieHandler
from handler.preferences_handler import PreferencesHandler, ChannelErrorState
from ui.ui_handler_main import UIHandlerMain, UICleaner
from ui.ui_handler_run import UIHandlerRun
from ui.ui_handler_settings import UIHandlerSettings
from watcher.watcher_data_container import WatcherInputDataContainer


class App():
    def __init__(self):
        self.preference_handler = PreferencesHandler()
        self.cookie_handler = CookieHandler()
        self.options = self.preference_handler.options
        self.channels = self.preference_handler.channels
        self.cookie_data = self.cookie_handler.cookie_data

    def _run_on_start(self):
        UIHandlerMain.show_logo()
        # do countdown
        if UIHandlerMain.run_on_start_countdown():
            # run watcher
            UIHandlerMain.show_logo()
            on_start_input_data_container = WatcherInputDataContainer(self.channels, self.cookie_data)
            UIHandlerRun(on_start_input_data_container).run()

    def run(self):
        are_cookies_loaded = self.cookie_handler.load_from_file() is None
        are_preferences_loaded = self.preference_handler.load_from_file() is None

        if self.options.get("app_run_on_start"):
            self._run_on_start()
        ui_handler = UIHandlerMain(are_cookies_loaded, are_preferences_loaded, self.options, self.channels)
        while True:
            option = ui_handler.run()
            ui_handler.print_ui = True
            ui_handler.clear_console = True
            match option:
                case 1:
                    # run watcher
                    if self.channels and self.cookie_data:
                        UIHandlerMain.show_logo()
                        input_data_container = WatcherInputDataContainer(self.channels,
                                                                         self.cookie_data)
                        UIHandlerRun(input_data_container).run()
                    else:
                        ui_handler.on_begin_run_fail()
                case 2:
                    # add new channel
                    UICleaner.clear_console()
                    UIHandlerMain.show_logo()
                    print(" - Add new channel menu")
                    ui_handler.print_channel_bar(self.channels)
                    while True:
                        channel_to_add = UIHandlerSettings.input_channel()
                        if channel_to_add is None:
                            break
                        print("")
                        print(" Channel added successfully." if self.preference_handler.channel_add(channel_to_add) is None
                              else " Channel already exists.")
                    ui_handler.update(self.options, self.channels)
                case 3:
                    # remove channel
                    UICleaner.clear_console()
                    UIHandlerMain.show_logo()
                    print(" - Remove a channel menu")
                    ui_handler.print_channel_bar(self.channels)
                    while True:
                        channel_to_remove = UIHandlerSettings.input_channel()
                        if channel_to_remove is None:
                            break
                        print("")
                        print(" Channel removed successfully."
                              if self.preference_handler.channel_remove(channel_to_remove)
                              is None else " Channel does not exist.")
                case 4:
                    # move channel up
                    UICleaner.clear_console()
                    UIHandlerMain.show_logo()
                    print(" - Move channel up menu")
                    ui_handler.print_channel_bar(self.channels)
                    while True:
                        channel_to_move = UIHandlerSettings.input_channel()
                        if channel_to_move is None:
                            break
                        move_result = self.preference_handler.channel_move_up(channel_to_move)
                        print("")
                        if move_result is None:
                            print(" Channel moved up successfully.")
                            ui_handler.print_channel_bar(self.channels)
                        if move_result == ChannelErrorState.CHANNEL_ALREADY_ON_TOP:
                            print(" Channel is already on top.")
                        if move_result == ChannelErrorState.CHANNEL_DOES_NOT_EXIST:
                            print(" Channel does not exist.")
                case 5:
                    # move channel down
                    UICleaner.clear_console()
                    UIHandlerMain.show_logo()
                    print(" - Move channel down menu")
                    ui_handler.print_channel_bar(self.channels)
                    while True:
                        channel_to_move = UIHandlerSettings.input_channel()
                        if channel_to_move is None:
                            break
                        move_result = self.preference_handler.channel_move_down(channel_to_move)
                        print("")
                        if move_result is None:
                            print(" Channel moved down successfully.")
                            ui_handler.print_channel_bar(self.preference_handler.channels)
                        if move_result == ChannelErrorState.CHANNEL_ALREADY_ON_BOTTOM:
                            print(" Channel is already on bottom.")
                        if move_result == ChannelErrorState.CHANNEL_DOES_NOT_EXIST:
                            print(" Channel does not exist.")
                    ui_handler.print_ui = True
                case 6:
                    # toggle run on start
                    UICleaner.clear_console()
                    self.preference_handler.option_set("app_run_on_start",
                                                   not self.preference_handler.options.get("app_run_on_start"))
                case 7:
                    # toggle save on exit
                    UICleaner.clear_console()
                    self.preference_handler.option_set("app_save_on_exit",
                                                   not self.preference_handler.options.get("app_save_on_exit"))
                case 8:
                    # save preferences and cookies to file
                    if self.preference_handler.save_to_file() is None:
                        print(" Preferences saved successfully")
                    else:
                        print(" Error saving preferences")
                    if self.preference_handler.save_to_file() is None:
                        print(" Cookies saved successfully")
                    else:
                        print(" Error saving cookies")
                    print("")
                    ui_handler.print_ui = False
                    ui_handler.clear_console = False
                case 9:
                    # load cookies from clipboard
                    UICleaner.clear_console()
                    UIHandlerMain.show_logo()
                    print(" - Load cookies from clipboard menu")
                    while True:
                        cookie_file = UIHandlerSettings.input_cookie_json_file()
                        if cookie_file is None:
                            break
                        print(" Cookies loaded successfully." if self.cookie_handler.load_from_string(cookie_file) is None
                              else " Invalid cookie JSON. Try again.")
                case 0:
                    # exit
                    UICleaner.clear_console()
                    UIHandlerMain.show_logo()
                    if self.preference_handler.options.get("app_save_on_exit"):
                        if self.preference_handler.save_to_file() is None:
                            print(" Preferences saved successfully")
                        if self.cookie_handler.save_to_file() is None:
                            print(" Cookies saved successfully")
                    print(" Exiting\n")
                    sys.exit(0)
                case _:
                    print(" Invalid option. Try again.")