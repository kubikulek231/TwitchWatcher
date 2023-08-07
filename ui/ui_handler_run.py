import os
import time

import keyboard

from misc.is_rpi4 import IsARM
from ui.ui_handler_main import UIHandlerMain, UICleaner
from ui.ui_handler_run_data import UIDataManager
from watcher.watcher_data_container import WatcherInputDataContainer
from watcher.watcher_main import Watcher


class UIHandlerRun:
    def __init__(self, input_data_container: WatcherInputDataContainer):
        self._running = True
        self._stopping = False
        self._watcher = Watcher(input_data_container)
        self._channels = input_data_container.channels

    def _watcher_working(self) -> None:
        UICleaner.clear_console()
        UIHandlerMain.show_logo()
        print(" - Channels")
        UIHandlerMain.print_channel_bar(self._channels, end="\n")
        print(f" {UIDataManager.get_current_time_string()} @User: watcher START requested")
        print("           Press the ESC key to stop anytime")
        try:
            self._watcher.start()
            data_manager = UIDataManager()
            while self._running:
                data_manager.update_data(self._watcher.get_output_data())
                data_manager.show_data()
                time.sleep(1)
            self._watcher.stop()
        except Exception as e:
            print(e)

    def _on_key_release(self, event: keyboard.KeyboardEvent) -> None:
        if event.name == 'esc' and not self._stopping:
            self._running = False
            self._stopping = True
            print()
            print(f" {UIDataManager.get_current_time_string()} @User: watcher STOP requested")

    @staticmethod
    def _is_webdriver_present(driver_file_name: str = "chromedriver") -> bool:
        if os.name == "nt":  # Windows
            driver_path = f"driver/{driver_file_name}.exe"
        else:  # Assuming other OS (Linux, macOS, etc.)
            driver_path = f"driver/{driver_file_name}"
        if IsARM.is_arm():
            driver_path = "/usr/bin/chromedriver"
        return os.path.exists(driver_path)

    def run(self) -> None:
        if self._is_webdriver_present():
            listener = keyboard.on_release(callback=self._on_key_release)
            self._watcher_working()
            keyboard.unhook(listener)
            print(f"\n {UIDataManager.get_current_time_string()} @User: watcher STOPPED successfully\n")
        else:
            print(f"\n {UIDataManager.get_current_time_string()} @User: browser webdriver not found\n")

        for i in range(5, 0, -1):
            print(f" Exiting in {i}")
            time.sleep(1)
