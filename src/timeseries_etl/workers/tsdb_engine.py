from queue import Queue, Empty
import threading
import os
import os.path
from datetime import datetime
from typing import Sequence
import shutil
import logging
from typing import Callable

from tinyflux import TinyFlux, Point


class Engine:
    def __init__(self, config, log: Callable[[str], logging.Logger]):
        self._log = log(__name__)
        self._tinyflux_path = config.TINYFLUX_PATH
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
            if self._worker_thread.is_alive():
                self._log.debug(f"worker ({self.__class__.__name__}) is alive")
                return True
            else:
                self._log.debug("worker ({self.__class__.__name__}) is dead")
                return False
        else:
            self._log.debug("worker ({self.__class__.__name__}) is gone")
            return False

    def start_worker(self):
        self._exit_worker = False
        if not self._is_worker_alive():
            self._worker_thread = threading.Thread(target=self._worker)
            self._worker_thread.start()
            self._log.debug("worker ({self.__class__.__name__}) started")
        else:
            self._log.debug("worker ({self.__class__.__name__}) already started")

        return True

    def stop_worker(self):
        self._exit_worker = True
        if self._is_worker_alive():
            self._log.debug("worker ({self.__class__.__name__}) stopping")
            self._worker_thread.join()
            self._log.debug("worker ({self.__class__.__name__}) stopped")
        else:
            self._log.debug("worker ({self.__class__.__name__}) already stopped")
        return True

    def queue_size(self):
        queue_size = self._queue.qsize()
        self._log.debug("({self.__class__.__name__}) queue size: {queue_size}")
        return queue_size

    def insert(self, item: Point) -> None:
        self._queue.put(item)

    def insert_many(self, items: Sequence[Point]) -> None:
        for item in items:
            self.insert(item)

    # methods for context manager
    def __enter__(self):
        self.start_worker()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_worker()


class EngineMaintenance:
    def __init__(self, engine: Engine):
        self._engine = engine

    def run(self):
        self._engine.stop_worker()
        if os.path.exists(self._engine._tinyflux_path):
            self._backup()
        self._engine.start_worker()

    def _backup(self):
        shutil.copyfile(
            self._engine._tinyflux_path,
            self._engine._tinyflux_path
            + f'.bak-{datetime.now().strftime("%Y%m%d%H%M%S")}',
        )
