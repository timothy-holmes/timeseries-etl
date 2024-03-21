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
        "PARAMS": BOMConfig,
        "SITES": BOMConfig,
        "DEFAULT_TIMEOUT": BOMConfig,
        "TAPO_USERNAME": P110Config,
        "TAPO_PASSWORD": P110Config,  # needs to be set at run time
    }
    for var in required_vars:
        class_name = required_vars[var].__class__.__name__
        assert hasattr(
            required_vars[var], var
        ), f"Missing required variable: {var} in {class_name}"
