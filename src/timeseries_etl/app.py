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
    # singleton/services
    sched = ScheduleWorker(config=SchedulerConfig)
    engine = Engine(config=EngineConfig)
    engine_maintenance = EngineMaintenance(engine=engine)
    bom = ExtractorBOM(config=BOMConfig)

    # workers
    sched.start_worker()
    engine.start_worker()

    # schuedled jobs
    def engine_maintenance_job(engine_maintenance_service):
        engine_maintenance_service.run()

    def bom_job(bom_service, engine_service):
        for p in bom_service.get_points():
            engine_service.insert(p)

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

    # hot start
    schedule.run_all(delay_seconds=10)

    # run
    while True:
        schedule.run_pending()
        time.sleep(1)
