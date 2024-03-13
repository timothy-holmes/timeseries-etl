from queue import Queue
import threading

from tinyflux import TinyFlux

from config import Config


class Engine:
    def __init__(self, tinyflux_path):
        self._tinyflux_path = tinyflux_path
        self.queue = Queue()

    def _start_worker(self):
        self.exit_worker = False
        self.worker_thread = threading.Thread(target=self._worker)
        self.worker_thread.start()
        return True

    def _stop_worker(self):
        self.exit_worker = True
        self.worker_thread.join()
        return True

    def _worker(self):
        with TinyFlux(self._tinyflux_path) as db:
            while not self.exit_worker:
                if not self.queue.empty():
                    item = self.queue.get()
                    db.insert(item)

    def close(self):
        self._stop_worker()
