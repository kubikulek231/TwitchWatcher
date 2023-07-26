import json
from enum import Enum
import os


class PreferencesJsonErrorState(Enum):
    PREFERENCES_FILE_NOT_FOUND = "Preferences file not found."
    PREFERENCES_FAILED_TO_DECODE = "Failed to decode preferences JSON file."
    PREFERENCES_FAILED_TO_SAVE = "Failed to save preferences JSON file."
    PREFERENCES_SAVE_DIRECTORY_NOT_FOUND = "Failed to locate save preferences directory."
    PREFERENCES_SAVE_PATH_IS_DIRECTORY = "Preferences save path is a directory."
    PREFERENCES_SAVE_PERMISSION_DENIED = "Preferences save permission denied."
    PREFERENCES_UNHANDLED_EXCEPTION_OCCURRED = "Preferences save/load unhandled exception."


class ChannelErrorState(Enum):
    CHANNEL_DOES_NOT_EXIST = "Channel does not exist."
    CHANNEL_ALREADY_EXISTS = "Cannot add a channel that already exists."
    CHANNEL_NAME_IS_EMPTY = "Channel name cannot be empty."


class PreferencesHandler:
    def __init__(self):
        self.options = {"app_run_on_start": False}
        self._channels = []

    @property
    def channels(self):
        return self._channels

    def channel_add(self, channel_name: str):
        if channel_name == "":
            return ChannelErrorState.CHANNEL_NAME_IS_EMPTY
        if channel_name in self._channels:
            return ChannelErrorState.CHANNEL_ALREADY_EXISTS
        self._channels.append(channel_name)
        return None

    def channel_remove(self, channel_name: str):
        if channel_name == "":
            return ChannelErrorState.CHANNEL_NAME_IS_EMPTY
        if channel_name not in self._channels:
            return ChannelErrorState.CHANNEL_DOES_NOT_EXIST
        self._channels.remove(channel_name)
        return None

    def channel_move_to_top(self, channel_name: str):
        if channel_name == "":
            return ChannelErrorState.CHANNEL_NAME_IS_EMPTY
        if channel_name not in self._channels:
            return ChannelErrorState.CHANNEL_DOES_NOT_EXIST
        self._channels.remove(channel_name)
        self._channels.insert(0, channel_name)
        return None

    def save_preferences_to_file(self, path: str = "data/preferences.json"):
        try:
            directory = os.path.dirname(path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(path, "w+") as file:
                json.dump(self.preferences, file)
        except FileNotFoundError:
            return PreferencesJsonErrorState.PREFERENCES_SAVE_DIRECTORY_NOT_FOUND
        except IsADirectoryError:
            return PreferencesJsonErrorState.PREFERENCES_SAVE_PATH_IS_DIRECTORY
        except PermissionError:
            return PreferencesJsonErrorState.PREFERENCES_SAVE_PERMISSION_DENIED
        except Exception as e:
            print(e)
            return PreferencesJsonErrorState.PREFERENCES_UNHANDLED_EXCEPTION_OCCURRED
        return None

    def load_preferences_from_file(self, path: str = "data/preferences.json"):
        try:
            json_file = open(path, "r")
            self.preferences = json.load(json_file)
            json_file.close()
        except FileNotFoundError:
            return PreferencesJsonErrorState.PREFERENCES_SAVE_DIRECTORY_NOT_FOUND
        except json.JSONDecodeError:
            return PreferencesJsonErrorState.PREFERENCES_FAILED_TO_DECODE
        except Exception:
            return PreferencesJsonErrorState.PREFERENCES_UNHANDLED_EXCEPTION_OCCURRED
        return None
