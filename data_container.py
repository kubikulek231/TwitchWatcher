

class WatcherInputDataContainer:
    def __init__(self, channels: list, cookie_data: dict):
        self.channels = channels
        self.cookie_data = cookie_data


class WatcherOutputDataContainer:
    def __init__(self):
        self.routine_state = None
        self.critical_error = False
        self.stream_name = None
        self.stream_game = None
        self.stream_title = None
        self.stream_viewers = None
        self.chat_points = None
        self.chat_claimed_num = None
        self.latest_drop_name = None
        self.latest_drop_game = None
        self.latest_drop_time = None
