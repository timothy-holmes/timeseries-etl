from datetime import datetime, timedelta
import time

from tinyflux import Point

from tsdb.engine import Engine

TEST_TINYFLUX_PATH = "./tests/data/test.db"


def test_worker_starts_and_stops():
    engine = Engine(TEST_TINYFLUX_PATH)
    engine._start_worker()
    assert engine._worker_alive() is True
    engine._stop_worker()
    assert engine._worker_alive() is False
    engine.close()


def test_insert_and_queue_size():
    engine = Engine(TEST_TINYFLUX_PATH)
    point1 = Point(
        time=datetime.now() - timedelta(seconds=1),
        measurement="measurement1",
        tags={"tag1": "value1"},
        fields={"field1": 10},
    )
    point2 = Point(
        time=datetime.now() + timedelta(seconds=1),
        measurement="measurement2",
        tags={"tag2": "value2"},
        fields={"field2": 20},
    )

    engine.insert(point1)
    engine.insert(point2)

    assert engine.queue_size() == 2

    engine._start_worker()
    time.sleep(1)

    assert engine.queue_size() == 0


def test_close():
    engine = Engine(TEST_TINYFLUX_PATH)
    engine._start_worker()
    engine.close()
    assert engine._worker_alive() == False
