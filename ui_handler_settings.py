from safe_input import SafeInput


class UIHandlerSettings:

    @staticmethod
    def input_channel_name() -> str:
        print(" Press ESC to return.")
        safe_input = SafeInput()
        while True:
            try:
                channel = safe_input.safe_input(" Enter channel name: ")
                if channel is None:
                    break
                if channel == "":
                    print(" Channel cannot be empty.")
                    continue
                return channel
            except ValueError:
                print(" Invalid channel. Try again.")

    @staticmethod
    def input_cookie_json_file() -> str:
        safe_input = SafeInput()
        while True:
            try:
                print(" Press ESC to return.")
                cookie_file = safe_input.safe_input(" Paste cookie JSON from clipboard: ")
                if cookie_file is None:
                    break
                if cookie_file == "":
                    print(" Cookie JSON cannot be empty.")
                    continue
                return cookie_file
            except ValueError:
                print(" Invalid cookie JSON. Try again.")



