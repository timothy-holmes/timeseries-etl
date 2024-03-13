from config import Config as c


def test_vars_available():
    required_vars = [
        "TINYFLUX_PATH",
        "TINYFLUX_BACKUP_PATH",
        "MQTT_ADDRESS",
        "MQTT_PORT",
    ]
    for var in required_vars:
        assert hasattr(c, var), f"Missing required variable: {var}"
