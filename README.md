# ETL service for HomeLab

## Purpose

Exhaustive data pipeline for projects. Integates self-hosted healthchecks/job notification service, scheduler.

## Roadmap
- dev container (fix git commit issue)
- pre-commit (not working with environment)
- black
- flake8
- pytest -> TDD (need to add pyproject.toml with pytest pythonpath entry)
- integrations:
    - BoM
    - P110 power usage
    - MQTT broker
    - Zigbee devices: temperature and humidity, air quality (via MQTT)
    - Shelly H&T (via MQTT)
    - solar power production
- tinyflux db maintenance ie. backup and remove duplicate points
- CI/CD pipeline
