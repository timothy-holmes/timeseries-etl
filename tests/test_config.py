from timeseries_etl.config import (
    EngineConfig,
    SchedulerConfig,
    BOMConfig,
    MQTTConfig,
    P110Config,
)


def test_vars_available():
    required_vars = {
        "TINYFLUX_PATH": EngineConfig,
        "MQTT_ADDRESS": MQTTConfig,
        "MQTT_PORT": MQTTConfig,
    }
    for var in required_vars:
        class_name = required_vars[var].__class__.__name__
        assert hasattr(
            required_vars[var], var
        ), f"Missing required variable: {var} in {class_name}"
