from datetime import datetime, timedelta
import time
import random
import string

import pytest
from tinyflux import Point

from timeseries_etl.workers.tsdb_engine import Engine, EngineMaintenance

@pytest.fixture
def mock_engine(temp_tinyflux_path, mock_log):
    with Engine(temp_tinyflux_path(), log=mock_log) as engine:
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
        yield engine

@pytest.fixture
def mock_engine_maintenance(mock_engine, mock_log):
    return EngineMaintenance(engine=mock_engine, log=mock_log)

def test_init(mock_engine_maintenance):
    assert mock_engine_maintenance._engine
    assert mock_engine_maintenance._log


def test_backup(mock_engine_maintenance):
    backup_path = mock_engine_maintenance._backup()
    assert len(backup_path) > len(mock_engine_maintenance._engine._tinyflux_path)
    assert backup_path.split(".")[-1].startswith(".bak")
    assert backup_path.startswith(mock_engine_maintenance._engine._tinyflux_path)

def test_run(mock_engine_maintenance):
    mock_engine_maintenance.run()