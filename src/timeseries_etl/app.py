import time

import schedule

from oversight import log
from timeseries_etl.workers.tsdb_engine import Engine, EngineMaintenance
from timeseries_etl.workers.sched import ScheduleWorker
from timeseries_etl.clients.bom_etl import ExtractorBOM
from timeseries_etl.config import (
    BOMConfig,
    SchedulerConfig,
    EngineConfig,
)


def main():
    # workers
    log.info('Starting "timeseries_etl"')

    with (
        ScheduleWorker(config=SchedulerConfig, log=log) as sched,
        Engine(config=EngineConfig, log=log) as engine,
    ):
        log.info('"timeseries_etl" started')

        # on-demand services
        engine_maintenance = EngineMaintenance(engine=engine, log=log)
        bom = ExtractorBOM(config=BOMConfig, log=log)

        try:
            set_schedule(sched, engine, engine_maintenance, bom)
            schedule.run_all(delay_seconds=10)
            log.info('"timeseries_etl" running')

            # run
            while True:
                schedule.run_pending()
                time.sleep(1)

        except KeyboardInterrupt:
            log.info("keyboard press -> exiting gracefully")
            pass


def set_schedule(sched, engine, engine_maintenance, bom):
    # job functions
    def bom_job(bom_service, engine_service):
        for p in bom_service.get_points():
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
