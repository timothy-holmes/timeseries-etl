import time

import schedule

from tsdb.engine import Engine, EngineMaintenance
from workers.sched import ScheduleWorker
from workers.bom_etl import ExtractorBOM

# from workers.p110_etl import ExtractorP110
from config import (
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

    schedule.every(1).days.at("12:00", tz="Australia/Melbourne").do(
        sched.run,
        item={
            "func": bom_job,
            "kwargs": {"bom_service": bom, "engine_service": engine},
        },
    )
    schedule.every(1).days.at("12:00", tz="Australia/Melbourne").do(
        sched.run,
        sched_service=sched,
        item={
            "func": bom_job,
            "kwargs": {"bom_service": bom, "engine_service": engine},
        },
    )


if __name__ == "__main__":
    # setup
    main()

    # hot start
    schedule.run_all(delay_seconds=10)

    # run
    while True:
        schedule.run_pending()
        time.sleep(1)
