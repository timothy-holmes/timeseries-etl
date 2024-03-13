import os


class Config:
    TINYFLUX_PATH = (
        os.environ.get("TINYFLUX_PATH") or "./data/bom-data.csv"
    )  # influx would look like this: http://localhost:4242/api/v2/write?bucket=tsdb
    MQTT_ADDRESS = os.environ.get("MQTT_ADDRESS") or "127.0.0.1"
    MQTT_PORT = os.environ.get("MQTT_PORT") or 1883
