import datetime
import threading
import logging

import requests
from tinyflux import Point

from timeseries_etl.clients.request import get_adapter


class ExtractorBOM:
    def __init__(self, config, log: logging.Logger) -> None:
        self._sites = config.SITES
        self._adapter = get_adapter(config)
        self._log = log

    def _get_site_obs(self, url, to_list) -> None:
        try:
            response = self._adapter.get(url)
            json_output = response.json()
        except requests.exceptions.JSONDecodeError:
            return

        data = json_output.get("observations", {}).get("data", [])
        self._log.info(f"Got {len(data)} observations from {url}")

        for ob in data:
            to_list.append(ob)

    @staticmethod
    def _ob_to_point(ob) -> Point:
        """
        Convert a weather observation into a data point.

        Args:
            ob (dict): The weather observation to convert into a data point.

        Returns:
            Point: A data point representing the weather observation.
        """
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
        """
        Retrieve all the data points extracted from BOM sites.

        Returns:
            list[Point]: A list of data points extracted from BOM sites.
        """
        result = []  # single operation (ie. append) is thread-safe
        threads = []

        self._log.info(f"Retrieving data from {len(self._sites)} sites...")

        for site in self._sites:
            thread = threading.Thread(
                target=self._get_site_obs,
                kwargs={"url": site["url"], "to_list": result},
            )
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        self._log.info(
            f"Retrieved {len(result)} observations from {len(self._sites)} sites"
        )

        return [self._ob_to_point(d) for d in result]
