from queue import Queue, Empty
import threading
import os, os.path
from datetime import datetime
from typing import Sequence

from tinyflux import TinyFlux, Point


class Engine:
    def __init__(self, tinyflux_path):
        self._tinyflux_path = tinyflux_path
        self._worker_thread = None
        self._exit_worker = False
        self._queue = Queue()

    def _worker(self) -> None:
        with TinyFlux(self._tinyflux_path) as db:
            while not self._exit_worker:
                if not self._queue.empty():
                    try:
                        item = self._queue.get(timeout=1)
                    except Empty:
                        pass
                    else:
                        db.insert(item)

    def _is_worker_alive(self) -> bool:
        if self._worker_thread:
            return self._worker_thread.is_alive()
        else:
            return False

    def start_worker(self) -> None:
        """Blocking method to start worker. Worker is started on return."""
        self._exit_worker = False
        if not self._is_worker_alive():
            self._worker_thread = threading.Thread(target=self._worker)
            self._worker_thread.start()

    def stop_worker(self) -> None:
        """Blocking method to stop worker. Worker is stopped on return."""
        self._exit_worker = True
        if self._is_worker_alive():
            self._worker_thread.join()

    def queue_size(self) -> int:
        return self._queue.qsize()

    def insert(self, item: Point) -> None:
        self._queue.put(item)

    def insert_many(self, items: Sequence[Point]) -> None:
        for item in items:
            self.insert(item)


class EngineMaintenance:
    def __init__(self, engine: Engine):
        self._engine = engine

    def run(self):
        self._engine.stop_worker()
        if os.path.exists(self._engine._tinyflux_path):
            self._backup()
        self._engine.start_worker()

    def _backup(self):
        os.copy(
            self._engine._tinyflux_path,
            self._engine._tinyflux_path
            + f'.bak-{datetime.now().strftime("%Y%m%d%H%M%S")}',
        )
