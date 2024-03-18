import os
import json


class SchedulerConfig:
    LOOP_CYCLE_TIME = 1  # seconds


class EngineConfig:
    TINYFLUX_PATH = (
        os.environ.get("TINYFLUX_PATH") or "./data/data.csv"
    )  # influx would look like this: http://localhost:4242/api/v2/write?bucket=tsdb


class MQTTConfig:
    MQTT_ADDRESS = os.environ.get("MQTT_ADDRESS") or "127.0.0.1"
    MQTT_PORT = os.environ.get("MQTT_PORT") or 1883


class BOMConfig:
    PARAMS = json.load(open("../config/bom_params.json", "r"))
    SITES = [
        {
            "name": "Trentham (CFA)",
            "url": "http://www.bom.gov.au/fwo/IDV60801/IDV60801.99821.json",
        },
        {
            "name": "Ballan (CFA)",
            "url": "http://www.bom.gov.au/fwo/IDV60801/IDV60801.99820.json",
        },
        {
            "name": "Essendon Airport",
            "url": "http://www.bom.gov.au/fwo/IDV60801/IDV60801.95866.json",
        },
        {
            "name": "Kilmore Gap",
            "url": "http://www.bom.gov.au/fwo/IDV60801/IDV60801.94860.json",
        },
    ]
    DEFAULT_TIMEOUT = 5


class P110Config:
    pass
