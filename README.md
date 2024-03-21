# ETL service for HomeLab

## Purpose

Exhaustive data pipeline for projects. Integates self-hosted healthchecks/job notification service, scheduler.

## Quick start
### Development

Build and start container (if not running already):

```sh
    docker-compose -f ./docker/dev/docker-compose.yml build && \
    docker-compose -f ./docker/dev/docker-compose.yml up -d
```

- enter container using VS Code to attach
- open bash inside container: 
    `docker exec -it ts-etl-dev bash`
- run commands inside container when required:
    `docker exec -t ts-etl-dev pytest`

### Production

Build and start container:

```sh
    docker-compose -f ./docker/prod/docker-compose.yml build && \
    docker-compose -f ./docker/prod/docker-compose.yml up -d
```

## Roadmap
- Dev container (to run tests, linting etc.)
    - Pre-commit?
    - Black
    - Flake8
    - Pytest (need to add pyproject.toml with pytest pythonpath entry)
- Integrations:
    - BoM (scheduled for every day)
    - P110 power usage (scheduled for every 5 seconds)
    - MQTT broker
    - Zigbee devices: temperature and humidity, air quality; via MQTT (subscription)
    - Shelly H&T via MQTT (subscription)
    - solar power production (scheduled, TBD)
- Tinyflux db maintenance mode
    - Start temporary db worker, change queue
    - Stop permanent worker
    - Do maintenance (eg. backup and remove duplicate points)
    - Start permanent worker, change queue
    - Migrate temp data
    - Stop temporary worker, delete temp db
- Data reports (job)
- CI/CD pipeline

## First release (v0.1.0)
- DB worker written
- BoM integration done
- Pytest, tests written
- Scheduler is supervising
