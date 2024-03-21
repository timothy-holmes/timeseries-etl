import asyncio
from datetime import datetime, timedelta
import logging

from plugp100.api.tapo_client import TapoClient
from plugp100.common.credentials import AuthCredential
from tinyflux import Point


class P110Client:
    def __init__(self, config, log: logging.Logger):
        self._tapo_ip = config.TAPO_ADDRESS
        self._credentials = AuthCredential(config.TAPO_USERNAME, config.TAPO_PASSWORD)
        self._time_diff = self._get_time_diff()
        self._log = log

    def _get_p110_power(self):
        tapo = TapoClient.create(self._credentials, self._tapo_ip)
        response = asyncio.run(tapo.get_current_power())
        return response.value.current_power

    def _get_time_diff(self):
        tapo = TapoClient.create(self._credentials, self._tapo_ip)
        response = asyncio.run(tapo.get_device_info())
        return response.value.get("time_diff")

    def get_point(self):
        return self._power_to_point(
            current_power=self._get_p110_power()
        )

    def _power_to_point(self, current_power):
        return Point(
            time=datetime.now() + timedelta(minutes=self._time_diff),
            measurement="power_usage",
            tags={"site": "p110", "devices_connected": "home-server,"},
            fields={"current_power": current_power},
        )
