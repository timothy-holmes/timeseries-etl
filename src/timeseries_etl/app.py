import time
from datetime import datetime, timedelta

import schedule
import requests

from timeseries_etl.oversight import configured_logger
from timeseries_etl.workers.tsdb_engine import Engine, EngineMaintenance
from timeseries_etl.workers.sched import ScheduleWorker
from timeseries_etl.clients.bom_etl import ExtractorBOM
from timeseries_etl.clients.p110 import P110Client
from timeseries_etl.config import (
    BOMConfig,
    SchedulerConfig,
    EngineConfig,
    P110Config,
)


# job functions
def bom_job(bom_service, engine_service):
    for p in bom_service.get_points():
        engine_service.insert(p)


def p110_job(p110_service, engine_service):
    for p in p110_service.get_point():
        engine_service.insert(p)


def start_up(log):
    log.info("Running start-up job")
    return schedule.CancelJob


def main():
    # workers
    log = configured_logger(__name__)
    log.info('Starting "timeseries_etl"')

    with Engine(config=EngineConfig, log=configured_logger) as engine:
        log.info('"timeseries_etl" started')

        # on-demand services
        engine_maintenance = EngineMaintenance(engine=engine, log=configured_logger)
        bom = ExtractorBOM(config=BOMConfig, log=configured_logger)
        p110 = P110Client(config=P110Config, log=configured_logger)

        near_future = (datetime.now() + timedelta(seconds=60)).strftime("%H:%M:%S")
        schedule.every(1).days.at("12:00").do(
            bom_job, bom_service=bom, engine_service=engine
        )
        schedule.every(1).days.at("13:00").do(engine_maintenance.run)
        schedule.every(1).minutes.do(p110_job, p110_service=p110, engine_service=engine)
        schedule.every().day.at(near_future).do(start_up, log=log)

        schedule.run_all(delay_seconds=10)
        log.info('"timeseries_etl" running')

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            log.info("keyboard press -> exiting gracefully")
