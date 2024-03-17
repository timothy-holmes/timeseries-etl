from queue import Queue, Empty
import threading
import time

from tinyflux import TinyFlux, Point


class Engine:
    def __init__(self, tinyflux_path):
        self._tinyflux_path = tinyflux_path
        self._worker_thread = None
        self._exit_worker = False
        self._queue = Queue()

    def _worker(self):
        with TinyFlux(self._tinyflux_path) as db:
            while not self._exit_worker:
                if not self._queue.empty():
                    try:
                        item = self._queue.get(timeout=1)
                    except Empty:
                        pass
                    else:
                        db.insert(item)

    def _is_worker_alive(self):
        if self._worker_thread:
            return self._worker_thread.is_alive()
        else:
            return False

    def start_worker(self):
        self._exit_worker = False
        if not self._is_worker_alive():
            self._worker_thread = threading.Thread(target=self._worker)
            self._worker_thread.start()
        return True

    def stop_worker(self):
        self._exit_worker = True
        if self._is_worker_alive():
            self._worker_thread.join()
        return True

    def queue_size(self):
        return self._queue.qsize()

    def insert(self, item: Point):
        self._queue.put(item)

