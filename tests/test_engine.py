from datetime import datetime, timedelta
import time
import random
import string

import pytest
from tinyflux import Point

from timeseries_etl.workers.tsdb_engine import Engine


def temp_tinyflux_path():
    r = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))

    class Config:
        TINYFLUX_PATH = f"./tests/test_data/{r}-temp.db"

    return Config

@pytest.fixture
def mock_engine(mock_log):
    return Engine(temp_tinyflux_path(), log=mock_log)


def test_temp_db_path():
    path = temp_tinyflux_path().TINYFLUX_PATH
    assert path.endswith("-temp.db")
    assert path.startswith("./tests/data/")
    assert len(path) == 8 + len("./tests/data/") + len("-temp.db")
    assert path != temp_tinyflux_path()


def test_worker_starts_and_stops(mock_engine):
    engine = mock_engine
    engine.start_worker()
    assert engine._is_worker_alive() is True
    engine.stop_worker()
    assert engine._is_worker_alive() is False


def test_insert_and_queue_size(mock_engine):
    engine = mock_engine
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
    time.sleep(0.5)
    assert engine.queue_size() == 0

    engine.stop_worker()

@pytest.mark.skipif(
    "not config.getoption('longtest')", reason="need --longtest option to run"
)
def test_performance(mock_log):
    # wait until end of other tests
    time.sleep(10)
    num_points = 1000

    # setup timing
    prework_start = time.time()
    with Engine(temp_tinyflux_path(), log=mock_log) as engine:
        prework_result = time.time() - prework_start

        # create random points
        points = [
            Point(
                time=datetime.now() + timedelta(seconds=i),
                measurement="measurement2",
                tags={"tag2": "value2"},
                fields={"field2": random.randint(0, 100)},
            )
            for i in range(num_points)
        ]

        # insert points
        insertion_start = time.time()
        for point in points:
            engine.insert(point)
        while engine.queue_size() > 0:
            time.sleep(0.1)
        insertion_end = time.time() - insertion_start

    assert prework_result < 0.5, "TinyFlux engine not fast enough starting up"
    assert (
        insertion_end < 50
    ), f"TinyFlux engine not fast enough inserting {num_points} points"


def test_context_implementation(mock_log):
    with Engine(temp_tinyflux_path(), log=mock_log) as engine:
        assert engine._is_worker_alive() is True

    assert engine._is_worker_alive() is False
