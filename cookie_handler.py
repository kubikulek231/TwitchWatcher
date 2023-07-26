from json_handler import JsonFileHandler


class CookieHandler(JsonFileHandler):
    def __init__(self):
        super().__init__()
        self._cookie_data = None

    @property
    def cookie_data(self):
        return self._cookie_data

    def _repair_cookie_data(self):
        if self._cookie_data is None:
            return False
        for cookie in self._cookie_data:
            if "unspecified" in cookie["sameSite"] or "no_restriction" in cookie["sameSite"]:
                cookie["sameSite"] = "None"
        return True

    def load_from_file(self, path: str = "data/cookies.json"):
        super().load_from_file(path)
        self._repair_cookie_data()

    def load_from_string(self, string: str):
        super().load_from_string(string)

    def save_to_file(self, path: str = "data/cookies.json"):
        super().save_to_file(path)
