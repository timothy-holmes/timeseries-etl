from datetime import datetime, timedelta
import time
import random
import string

from tinyflux import Point

from tsdb.engine import Engine

def temp_tinyflux_path():
    r = ''.join(
        random.choices(
            string.ascii_lowercase + string.digits, 
            k=8
        )
    )
    return f"./tests/data/{r}-temp.db"


def test_worker_starts_and_stops():
    engine = Engine(temp_tinyflux_path())
    engine.start_worker()
    assert engine._is_worker_alive() is True
    engine.stop_worker()
    assert engine._is_worker_alive() is False

def test_insert_and_queue_size():
    engine = Engine(temp_tinyflux_path())
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

    engine.start_worker()
    time.sleep(1)

    assert engine.queue_size() == 0

    engine.stop_worker()


def test_close():
    engine = Engine(temp_tinyflux_path())
    engine.start_worker()
    assert engine._is_worker_alive() is True
    engine.stop_worker()
    assert engine._is_worker_alive() is False


def test_performance():
    pre = time.time()
    engine = Engine(temp_tinyflux_path())
    engine.start_worker()
    points = [Point(
        time=datetime.now() + timedelta(seconds=i),
        measurement="measurement2",
        tags={"tag2": "value2"},
        fields={"field2": random.randint(0, 100)},
    ) for i in range(1000)]
    pre_end = time.time() - pre
    for point in points:
        engine.insert(point)
    while engine.queue_size() > 0:
        time.sleep(0.1)
    end = time.time() - pre
    engine.stop_worker()
    assert False, f'{pre} {pre_end}, {end}'