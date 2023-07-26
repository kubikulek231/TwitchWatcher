import json
from enum import Enum
import os


class JsonErrorState(Enum):
    JSON_FILE_NOT_FOUND = "Json file not found."
    JSON_FAILED_TO_DECODE = "Failed to decode JSON file."
    JSON_FAILED_TO_SAVE = "Failed to save JSON file."
    JSON_SAVE_DIRECTORY_NOT_FOUND = "Failed to locate save json directory."
    JSON_SAVE_PATH_IS_DIRECTORY = "JSON save path is a directory."
    JSON_SAVE_PERMISSION_DENIED = "Json save permission denied."
    JSON_UNHANDLED_EXCEPTION_OCCURRED = "Json save/load unhandled exception occurred."


class JsonFileHandler:
    def __init__(self):
        self.debug = False

    def save_to_file(self, path: str):
        try:
            directory = os.path.dirname(path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(path, "w+") as json_file:
                json.dump(self.__dict__, json_file)
        except FileNotFoundError:
            return JsonErrorState.JSON_SAVE_DIRECTORY_NOT_FOUND
        except IsADirectoryError:
            return JsonErrorState.JSON_SAVE_PATH_IS_DIRECTORY
        except PermissionError:
            return JsonErrorState.JSON_SAVE_PERMISSION_DENIED
        except Exception as e:
            if self.debug:
                print(e)
            return JsonErrorState.JSON_UNHANDLED_EXCEPTION_OCCURRED
        return None

    def load_from_file(self, path: str):
        try:
            with open(path, "r") as json_file:
                self.__dict__.update(json.load(json_file))
        except FileNotFoundError:
            return JsonErrorState.JSON_SAVE_DIRECTORY_NOT_FOUND
        except json.JSONDecodeError:
            return JsonErrorState.JSON_FAILED_TO_DECODE
        except Exception as e:
            if self.debug:
                print(e)
            return JsonErrorState.JSON_UNHANDLED_EXCEPTION_OCCURRED
        return None

    def load_from_string(self,  json_string: str):
        try:
            self.__dict__.update(json.loads(json_string))
        except json.JSONDecodeError:
            return JsonErrorState.JSON_FAILED_TO_DECODE
        except Exception as e:
            if self.debug:
                print(e)
            return JsonErrorState.JSON_UNHANDLED_EXCEPTION_OCCURRED
        return None
