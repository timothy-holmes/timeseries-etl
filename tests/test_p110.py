import pytest

import timeseries_etl.clients.p110
from timeseries_etl.config import P110Config


@pytest.fixture
def new_p110(mock_log):
    p110_client = timeseries_etl.clients.p110.P110Client(
        config=P110Config, log=mock_log
    )
    return p110_client


def test_init(new_p110):
    assert new_p110._time_diff == 600


def test_power_to_point(new_p110):
    assert new_p110._power_to_point(0)


def test_get_point(new_p110):
    assert new_p110.get_point()
