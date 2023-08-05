import threading
from pynput import keyboard


class SafeInput:
    def __init__(self):
        self._KEY_TO_PRESS = keyboard.Key.esc

    def _on_key_release(self, key) -> None:
        if key == self._KEY_TO_PRESS:
            raise KeyboardInterrupt

    def _listen_for_esc(self):
        with keyboard.Listener(on_release=self._on_key_release) as listener:
            listener.join()

    def safe_input(self, prompt):
        t = threading.Thread(target=self._listen_for_esc)
        t.start()

        try:
            result = input(prompt)
        except KeyboardInterrupt:
            result = None

        t.join()
        return result
