import time

import schedule

from timeseries_etl.workers.tsdb_engine import Engine, EngineMaintenance
from timeseries_etl.workers.sched import ScheduleWorker
from timeseries_etl.clients.bom_etl import ExtractorBOM
from timeseries_etl.config import (
    BOMConfig,
    # P110Config,
    SchedulerConfig,
    EngineConfig,
)


def main():
    # workers
    with (
        ScheduleWorker(config=SchedulerConfig) as sched, 
        Engine(config=EngineConfig) as engine
    ):

        # non-threaded service
        engine_maintenance = EngineMaintenance(engine=engine)

        # client
        bom = ExtractorBOM(config=BOMConfig)

        try:
            set_schedule(sched, engine, engine_maintenance, bom)
            schedule.run_all(delay_seconds=10)

            # run
            while True:
                schedule.run_pending()
                time.sleep(1)

        except KeyboardInterrupt:
            pass


def set_schedule(sched, engine, engine_maintenance, bom):
    # job functions
    def engine_maintenance_job(engine_maintenance_service):
        engine_maintenance_service.run()

    def bom_job(bom_service, engine_service):
        for p in bom_service.get_points():
            engine_service.insert(p)

    # schedule entries
    schedule.every(1).days.at("12:00").do(
        sched.run,
        item={
            "func": bom_job,
            "kwargs": {"bom_service": bom, "engine_service": engine},
        },
    )
    schedule.every(1).days.at("13:00").do(
        sched.run,
        item={
            "func": engine_maintenance_job,
            "kwargs": {"engine_maintenance_service": engine_maintenance},
        },
    )
