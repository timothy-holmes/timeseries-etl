import json

import pytest
import responses
import genson
import requests
from tinyflux import Point

from timeseries_etl.clients.bom_etl import ExtractorBOM


@pytest.fixture
def sites():
    return [
        {"name": "Test Site 1", "url": "http://test_url/big-data"},
        {"name": "Test Site 2", "url": "http://test_url/big-data"},
    ]


@pytest.fixture
def single_observation():
    return json.load(open("tests/data/bom/single_observation.json"))


@pytest.fixture
def extractor(sites, mock_log):
    class Config:
        PARAMS = {"headers": {"Accept": "application/json"}, "cookies": {}}
        SITES = sites
        DEFAULT_TIMEOUT = 5
        # Add other configuration settings as needed

    return ExtractorBOM(Config, log=mock_log)


@pytest.fixture
def register_responses(sites):
    with responses.RequestsMock() as mock:
        for site in sites:
            mock.add(
                method=responses.GET,
                url=site["url"],
                content_type="application/json",
                json=json.load(open("tests/test_data/bom/excerpt.json")),
            )
        yield mock


@responses.activate
def test_get_site_obs(extractor):
    responses.add(
        responses.GET,
        "http://test_url/little-data",
        json={
            "observations": {
                "data": [{"observation": "test_A"}, {"observation": "test_B"}]
            }
        },
    )
    data_list = []
    extractor._get_site_obs("http://test_url/little-data", data_list)
    assert data_list == [{"observation": "test_A"}, {"observation": "test_B"}]


def test_ob_to_point(extractor, single_observation):
    point = extractor._ob_to_point(single_observation)
    assert point.fields["air_temp"] == 17.2
    assert point.fields["rel_hum"] == 60


def test_get_points(extractor, register_responses):
    points = extractor.get_points()
    assert isinstance(points, list)
    assert len(points) == 40
    assert isinstance(points[0], Point)


def test_bom_schema():
    """Validate the json data example matches the generated schema"""
    bom_schema = genson.SchemaBuilder()
    bom_schema.add_schema(json.load(open("tests/data/bom/schema/bom.schema.json")))
    example_schema = genson.SchemaBuilder()
    example_schema.add_schema(json.load(open("tests/data/bom/schema/bom.schema.json")))
    example_schema.add_object(json.load(open("tests/data/bom/excerpt.json")))
    assert bom_schema == example_schema


@pytest.mark.skipif(
    "not config.getoption('outside')", reason="need --outside option to run"
)
def test_bom_request():
    assert requests.get("http://google.com/").status_code == 200
