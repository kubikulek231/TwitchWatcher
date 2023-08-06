from ui.ui_handler_main import UICleaner, UIHandlerMain
from handler.preferences_handler import PreferencesHandler
from handler.cookie_handler import CookieHandler


class UIHandlerSettings:
    def __init__(self,  preference_handler: PreferencesHandler, cookie_handler: CookieHandler):
        self.preference_handler = preference_handler
        self.cookie_handler = cookie_handler
        self.options = self.preference_handler.options
        self.channels = self.preference_handler.channels
        self.cookie_data = self.cookie_handler.cookie_data

    @staticmethod
    def _clear_and_show_logo():
        UICleaner.clear_console()
        UIHandlerMain.show_logo()


    @staticmethod
    def input_channel() -> str:
        print("")
        print(" Enter '_' to return.")
        while True:
            try:
                channel = input(" Enter channel name: ")
                if channel == '_':
                    break
                if channel == "":
                    print(" Channel name cannot be empty.")
                    continue
                return channel
            except ValueError:
                print(" Invalid channel. Try again.")

    @staticmethod
    def input_cookie_json_file() -> str:
        print("")
        print(" Enter '_' to return.")
        while True:
            try:
                print(" Pasted JSON must have the compact format.")
                print(" Use online formatter like https://jsonformatter.curiousconcept.com/")
                cookie_file = input(" Paste cookie JSON from clipboard: ")
                print("")
                if cookie_file == '_':
                    break
                if cookie_file == "":
                    print(" Cookie JSON cannot be empty.")
                    continue
                return cookie_file
            except ValueError:
                print(" Invalid cookie JSON. Try again.")
