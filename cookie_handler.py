import os
import json
from enum import Enum


class CookieJsonErrorState(Enum):
    COOKIES_FILE_NOT_FOUND = "Cookies file not found."
    COOKIES_FAILED_TO_DECODE = "Failed to decode cookie JSON file."
    COOKIES_FAILED_TO_SAVE = "Failed to save cookie JSON file."
    COOKIES_SAVE_DIRECTORY_NOT_FOUND = "Failed to locate save cookie directory."
    COOKIES_SAVE_PATH_IS_DIRECTORY = "Cookie save path is a directory."
    COOKIES_SAVE_PERMISSION_DENIED = "Cookie save permission denied."
    COOKIES_UNHANDLED_EXCEPTION_OCCURRED = "Cookie save/load unhandled exception occurred."


class CookieHandler:
    def __init__(self):
        self._cookie_data = None

    def cookie_data(self):
        return self._cookie_data

    def load_cookies_from_file(self, path: str = "data/cookies.json"):
        try:
            json_file = open(path, "r")
            data = json.load(json_file)
            json_file.close()
            for cookie in data:
                if "unspecified" in cookie["sameSite"] or "no_restriction" in cookie["sameSite"]:
                    cookie["sameSite"] = "None"
            self._cookie_data = data
        except FileNotFoundError:
            return CookieJsonErrorState.COOKIES_FILE_NOT_FOUND
        except json.JSONDecodeError:
            return CookieJsonErrorState.COOKIES_FAILED_TO_DECODE
        except Exception:
            return CookieJsonErrorState.COOKIES_UNHANDLED_EXCEPTION_OCCURRED
        return None

    def load_cookies_from_string(self, string: str):
        try:
            data = json.loads(string.strip())
            for cookie in data:
                if "unspecified" in cookie["sameSite"] or "no_restriction" in cookie["sameSite"]:
                    cookie["sameSite"] = "None"
            self._cookie_data = data
        except json.JSONDecodeError:
            return CookieJsonErrorState.COOKIES_FAILED_TO_DECODE
        except Exception:
            return CookieJsonErrorState.COOKIES_UNHANDLED_EXCEPTION_OCCURRED
        return None

    def save_cookies_to_file(self, path: str = "data/cookies.json"):
        try:
            directory = os.path.dirname(path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(path, "w+") as file:
                json.dump(self._cookie_data, file)
        except FileNotFoundError:
            return CookieJsonErrorState.COOKIES_SAVE_DIRECTORY_NOT_FOUND
        except IsADirectoryError:
            return CookieJsonErrorState.COOKIES_SAVE_PATH_IS_DIRECTORY
        except PermissionError:
            return CookieJsonErrorState.COOKIES_SAVE_PERMISSION_DENIED
        except Exception as e:
            print(e)
            return CookieJsonErrorState.COOKIES_UNHANDLED_EXCEPTION_OCCURRED
        return None
