from enum import Enum
from json_handler import JsonFileHandler, JsonErrorState


class ChannelErrorState(Enum):
    CHANNEL_DOES_NOT_EXIST = "Channel does not exist."
    CHANNEL_ALREADY_EXISTS = "Cannot add a channel that already exists."
    CHANNEL_NAME_IS_EMPTY = "Channel name cannot be empty."


class PreferencesHandler(JsonFileHandler):
    def __init__(self):
        super().__init__()
        self.options = {"app_run_on_start": False}
        self._channels = []

    @property
    def channels(self):
        return self._channels

    def channel_add(self, channel_name: str) -> ChannelErrorState:
        if channel_name == "":
            return ChannelErrorState.CHANNEL_NAME_IS_EMPTY
        if channel_name in self._channels:
            return ChannelErrorState.CHANNEL_ALREADY_EXISTS
        self._channels.append(channel_name)

    def channel_remove(self, channel_name: str) -> ChannelErrorState:
        if channel_name == "":
            return ChannelErrorState.CHANNEL_NAME_IS_EMPTY
        if channel_name not in self._channels:
            return ChannelErrorState.CHANNEL_DOES_NOT_EXIST
        self._channels.remove(channel_name)

    def channel_move_to_top(self, channel_name: str) -> ChannelErrorState:
        if channel_name == "":
            return ChannelErrorState.CHANNEL_NAME_IS_EMPTY
        if channel_name not in self._channels:
            return ChannelErrorState.CHANNEL_DOES_NOT_EXIST
        self._channels.remove(channel_name)
        self._channels.insert(0, channel_name)

    def load_from_file(self, path: str = "data/preferences.json") -> JsonErrorState:
        return super().load_from_file(path)

    def save_to_file(self, path: str = "data/preferences.json") -> JsonErrorState:
        return super().save_to_file(path)
