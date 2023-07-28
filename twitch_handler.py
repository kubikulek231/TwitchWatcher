import html


class TwitchHandler:
    def __init__(self, browser_handler):
        self._browser_handler = browser_handler

    def twitch_login_page_open(self) -> bool:
        self._browser_handler.goto_page("https://www.twitch.tv/login")
        if self._browser_handler.element_is_present('//*[@id="login-username"]'):
            return True
        return False

    def twitch_is_logged(self) -> bool:
        element_name = self._browser_handler.element_get_name("body")
        if element_name is None or "logged-in" not in element_name:
            return True
        return False

    def twitch_stream_player_open(self, channel):
        self._browser_handler.browser_goto_page(
            f"https://player.twitch.tv/?channel={channel}&enableExtensions=true&muted=false&"
            f"parent=twitch.tv&player=popout&quality=160p30&volume=69")

    def twitch_stream_player_unmute(self) -> bool:
        return self._browser_handler.element_click('//*[@id="channel-player"]/div/div[1]/div[2]/div/div[1]/button')

    def twitch_stream_player_get_game(self) -> str:
        stream_game_xpath = '//a[@data-a-target="player-info-game-name"]'
        return self._browser_handler.element_get_text(stream_game_xpath)

    def twitch_stream_player_get_title(self) -> str:
        stream_game_xpath = '//p[@data-test-selector="stream-info-card-component__subtitle"]'
        return self._browser_handler.element_get_text(stream_game_xpath)

    def twitch_stream_player_get_viewers(self) -> str:
        stream_game_xpath = '//p[@data-test-selector="stream-info-card-component__description"]'
        viewer_count_string = self._browser_handler.element_get_text(stream_game_xpath)
        if viewer_count_string is not None:
            """for char in viewer_string:
                if char.isdigit():
                    viewer_number += char"""
            return html.unescape(viewer_count_string)

    def twitch_channel_is_online(self, channel) -> bool:
        self.twitch_stream_player_open(channel)
        if self._browser_handler.element_get_name(
                '//*[@id="root"]/div/div/div/div[1]/div/div[2]/div/div/div[3]'
                '/div[2]/div[1]/div/div/div[1]/div/div[1]/div/p') is None:
            return True
        return False

    def twitch_chat_open(self, channel) -> None:
        self._browser_handler.goto_page(
            f"https://www.twitch.tv/popout/{channel}/chat?popout=")

    def twitch_chat_get_points(self) -> str:
        points_value_xpath = '//*[@id="live-page-chat"]/div/div/div[2]/div/div/section/div/div[6]/div[2]/div[2]' \
                             '/div[1]/div/div/div[1]/div[1]/div[2]/button/div/div/div/div[2]/span'
        points_value = self._browser_handler.element_get_text(points_value_xpath)
        return html.unescape(points_value)

    def twitch_chat_is_claimable(self) -> bool:
        points_button_xpath = '//*[@id="root"]/div/div[1]/div/div/section/div/div[6]/div[2]/div[2]/div[1]' \
                              '/div/div/div/div[2]'
        if self._browser_handler.element_is_present(points_button_xpath) is not None:
            return False
        return True

    def twitch_chat_claim(self) -> bool:
        points_button_xpath = '//*[@id="root"]/div/div[1]/div/div/section/div/div[6]/div[2]/div[2]/div[1]' \
                              '/div/div/div/div[2]'
        return self._browser_handler.element_click(points_button_xpath)

    def twitch_drop_inventory_open(self) -> None:
        self._browser_handler.goto_page(
            "https://www.twitch.tv/drops/inventory")

    def twitch_drop_inventory_is_claimable(self) -> bool:
        drop_button_xpath = '//*[@id="root"]/div/div[2]/div/main/div[1]/div[3]/div/div/div/div/div/div[1]/div[3]' \
                            '/div[2]/div[2]/div/div[1]/div[1]/div/div/div[1]/div[2]/button'
        return self._browser_handler.element_is_present(drop_button_xpath)

    def twitch_drop_inventory_claim(self) -> bool:
        drop_button_xpath = '//*[@id="root"]/div/div[2]/div/main/div[1]/div[3]/div/div/div/div/div/div[1]/div[3]' \
                            '/div[2]/div[2]/div/div[1]/div[1]/div/div/div[1]/div[2]/button'
        return self._browser_handler.element_click(drop_button_xpath)

    def twitch_drop_inventory_latest_drop_get_name(self) -> str:
        last_drop_title_xpath = '//*[@id="root"]/div/div[2]/div/main/div[1]/div[3]/div/div/div/div/div/div[1]/div[4]' \
                                '/div[2]/div[1]/div/div[1]/div[2]/div[2]/p'
        return self._browser_handler.element_get_text(last_drop_title_xpath)

    def twitch_drop_inventory_latest_drop_get_game(self) -> str:
        last_drop_name_xpath = '//*[@id="root"]/div/div[2]/div/main/div[1]/div[3]/div/div/div/div/div/div[1]/div[4]' \
                               '/div[2]/div[1]/div/div[2]/p'
        return self._browser_handler.element_get_text(last_drop_name_xpath)

    def twitch_drop_inventory_latest_drop_get_date(self) -> str:
        last_drop_date_xpath = '//*[@id="root"]/div/div[2]/div/main/div[1]/div[3]/div/div/div/div/div/div[1]/div[4]' \
                               '/div[2]/div[1]/div/div[1]/div[2]/div[1]/div[1]/p'
        return self._browser_handler.element_get_text(last_drop_date_xpath)
