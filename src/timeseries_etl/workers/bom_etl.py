import datetime

import requests
from tinyflux import Point


class ExtractorBOM:
    def __init__(self, config):
        self._SITES = config.SITES
        self._PARAMS = config.PARAMS

    def _get_site_observations(self, url) -> list[dict]:
        return (
            requests.get(
                url, headers=self._PARAMS["headers"], params=self._PARAMS["cookies"]
            )
            .json()
            .get("observations")
            .get("data")
        )

    @staticmethod
    def _ob_to_point(ob) -> Point:
        # Datetime object that is "timezone-naive".
        ts = datetime.datetime.strptime(ob["local_date_time_full"], "%Y%m%d%H%M%S")

        # Tags as a dict of string/string key values.
        tags = {"source": "BOM", "loc_name": ob["name"]}

        # Fields as a dict of string/numeric key values.
        fields = {
            "air_temp": float(ob["air_temp"]),
            "rel_hum": float(ob["rel_hum"]),
        }

        # Initialize the Point with the above attributes.
        return Point(
            measurement="climate",
            time=ts,
            tags=tags,
            fields=fields,
        )

    def get_points(self) -> list[Point]:
        observations = [
            obs
            for site in self._SITES
            for obs in self._get_site_observations(site["url"])
        ]

        return [self._ob_to_point(ob) for ob in observations]
