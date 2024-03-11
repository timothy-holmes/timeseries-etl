# ETL service for HomeLab

## Purpose

Exhaustive data pipeline for projects. Integates self-hosted healthchecks/job notification service, scheduler.

## Roadmap
- dev container (fix git commit issue)
- pre-commit, including black (done)
- ETL for BOM (done)
- pytest -> TDD (need to add pyproject.toml with pytest pythonpath entry)
- webhook endpoint/MQTT server for edge devices (waiting for zigbee bridge to arrive)
- tinyflux db maintenance ie. backup and remove duplicate points
- CI/CD pipeline
