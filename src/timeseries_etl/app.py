import time

import schedule

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


def main():
    # workers
    log = configured_logger(__name__)
    log.info('Starting "timeseries_etl"')

    with (
        ScheduleWorker(config=SchedulerConfig, log=log) as sched,
        Engine(config=EngineConfig, log=log) as engine,
    ):
        log.info('"timeseries_etl" started')

        # on-demand services
        engine_maintenance = EngineMaintenance(engine=engine, log=log)
        bom = ExtractorBOM(config=BOMConfig, log=log)
        p110 = P110Client(config=P110Config, log=log)

        try:
            set_schedule(sched, engine, engine_maintenance, bom, p110)
            schedule.run_all(delay_seconds=10)
            log.info('"timeseries_etl" running')

            # run
            while True:
                schedule.run_pending()
                time.sleep(1)

        except KeyboardInterrupt:
            log.info("keyboard press -> exiting gracefully")
            pass


def set_schedule(sched, engine, engine_maintenance, bom, p110):
    # job functions
    def bom_job(bom_service, engine_service):
        for p in bom_service.get_points():
            engine_service.insert(p)

    def p110_job(p110_service, engine_service):
        for p in p110_service.get_points():
            engine_service.insert(p)

    # schedule entries
    log.info("scheduling BoM scrapes")
    schedule.every(1).days.at("12:00").do(
        sched.add_job,
        item={
            "func": bom_job,
            "kwargs": {"bom_service": bom, "engine_service": engine},
        },
    )

    log.info("scheduling DB engine maintenance")
    schedule.every(1).days.at("13:00").do(
        sched.add_job,
        item={"func": engine_maintenance.run},
    )

    log.info("scheduling P110 scrapes")
    schedule.every(1).minutes.do(
        sched.add_job,
        item={
            "func": p110_job,
            "kwargs": {"p110_service": p110, "engine_service": engine},
        },
    )
