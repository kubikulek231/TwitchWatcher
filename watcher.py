import multiprocessing
import time
from data_container import DataContainer

class Watcher:
    def __init__(self):
        self.running = False
        self._process = None

    def start(self, data_container: DataContainer):
        if self.running:
        self.running = True
        self._process = multiprocessing.Process(target=self._run(data_container))
        process.start()

    def stop(self):
        self.running = False

    def _run(self, data_container):
        while self.running:
            print(data_container)
            time.sleep(3)
