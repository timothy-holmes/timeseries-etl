from queue import Queue
import threading

from tinyflux import TinyFlux, Point


class Engine:
    def __init__(self, tinyflux_path):
        self._tinyflux_path = tinyflux_path
        self.queue = Queue()
        self._worker_thread = None
        self._exit_worker = False

    def _start_worker(self):
        self.exit_worker = False
        self.worker_thread = threading.Thread(target=self._worker)
        self.worker_thread.start()
        return True

    def _stop_worker(self):
        self.exit_worker = True
        if self.worker_thread:
            self.worker_thread.join()
        return True

    def _worker(self):
        with TinyFlux(self._tinyflux_path) as db:
            while not self.exit_worker:
                if not self.queue.empty():
                    item = self.queue.get()
                    db.insert(item)

    def _worker_alive(self):
        if self.worker_thread:
            return self.worker_thread.is_alive()
        else:
            return False

    def queue_size(self):
        return self.queue.qsize()

    def insert(self, item: Point):
        self.queue.put(item)

    def close(self):
        self._stop_worker()
