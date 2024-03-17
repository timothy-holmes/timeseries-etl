from typing import Callable
from queue import Queue, Empty
import threading

# TODO: rework to run job in parallel, currently running sequentially

class ScheduleWorker:
    def __init__(self, config):
        self._config = config
        self._worker_thread = None
        self._exit_worker = False
        self._queue = Queue()

    def _worker(self):
        while not self._exit_worker:
            if not self._queue.empty():
                try:
                    item = self._queue.get(timeout=1)
                except Empty:
                    pass
                else:
                    # health check/job log
                    item['func'](*item.get('args'), **item.get('kwargs'))
                    # health check/job log stop

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

    def insert(self, item: dict[str, Callable | list | dict]):
        self._queue.put(item)