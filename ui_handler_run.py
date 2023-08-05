import time

from pynput import keyboard

from ui_handler_run_data import UIDataManager
from watcher import Watcher
from watcher_data_container import WatcherInputDataContainer


class UIHandlerRun:
    def __init__(self, input_data_container: WatcherInputDataContainer):
        self._running = True
        self._stopping = False
        self._watcher = Watcher(input_data_container)

    def _watcher_working(self) -> None:
        print()
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

    def _on_key_release(self, key) -> None:
        if key == keyboard.Key.esc and not self._stopping:
            self._running = False
            self._stopping = True
            print()
            print(f" {UIDataManager.get_current_time_string()} @User: watcher STOP requested")

    def run(self) -> None:
        listener = keyboard.Listener(on_release=self._on_key_release)
        listener.start()
        self._watcher_working()
        listener.stop()
        print()
        print(f" {UIDataManager.get_current_time_string()} @User: watcher STOPPED successfully")
        print()
        for i in range(5, 0, -1):
            print(f" Exiting in {i}")
            time.sleep(1)
