import os


class UICleaner:

    @staticmethod
    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')


class UIHandlerMain:
    def __init__(
        self,
        are_cookies_loaded: bool,
        are_preferences_loaded: bool,
        cookies: dict,
        options: dict,
        channels: list,
    ):
        self.are_cookies_loaded = are_cookies_loaded
        self.are_preferences_loaded = are_preferences_loaded
        self.cookies = cookies
        self.options = options
        self.channels = channels

    @staticmethod
    def _show_logo() -> None:
        print("---------------------------------------------\n"
              "                 TwitchWatcher               \n"
              "---------------------------------------------")

    def _show_info(self) -> None:
        print(" Status:")
        print(f" Preferences: {'successfully' if self.are_preferences_loaded else 'not '} loaded")
        print(f" Cookies: {'successfully' if self.are_cookies_loaded else 'not '} loaded")

    def _show_channels(self) -> None:
        channel_list = self.channels
        print("---------------------------------------------\n"
              " Channels:")

        if not channel_list:
            print(" No channels added.")
            return

        channels_per_line = 3
        channel_string = ""
        for i, channel in enumerate(channel_list, 0):
            if i != 0:
                channel_string += ","
            if i % channels_per_line == 0 and i != 0:
                channel_string += "\n"
            channel_string += f" ({i+1}){channel}"
        print(channel_string)

    def _show_options(self) -> None:
        options = [
            "---------------------------------------------",
            " 1)   Run",
            " 2)   Add new channel",
            " 3)   Remove channel",
            f" 4)   Run on startup: {self.options['app_run_on_start']}",
            f" 5)   Save on exit: {self.options['app_save_on_exit']}",
            " 6)   Save current settings",
            " 7)   Load cookies from clipboard",
            " 0)   Exit",
            "---------------------------------------------"
        ]

        options_string = "\n".join(options)
        print(options_string)

    @staticmethod
    def _get_option() -> int:
        while True:
            try:
                option = int(input("Enter option: "))
                if option in range(8):
                    return option
                else:
                    print("Invalid option. Try again.")
            except ValueError:
                print("Invalid option. Try again.")

    def run(self) -> int:
        UICleaner.clear_console()
        self._show_logo()
        self._show_info()
        self._show_channels()
        self._show_options()
        option = self._get_option()
        UICleaner.clear_console()
        return option



