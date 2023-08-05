class UIHandlerSettings:

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
