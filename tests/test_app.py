import time
from datetime import datetime, timedelta

import schedule

from timeseries_etl.oversight import configured_logger
from timeseries_etl.app import bom_job, p110_job, start_up


def test_app(mock_app_engine, mock_bom, mock_p110, mock_log):
    log = configured_logger("test_log_app")
    engine = mock_app_engine(log)

    schedule.every(1).seconds.do(
        bom_job, bom_service=mock_bom(log), engine_service=engine
    )
    schedule.every(1).seconds.do(
        p110_job, p110_service=mock_p110(log), engine_service=engine
    )
    schedule.every(1).seconds.do(start_up, log=mock_log())
    schedule.run_all()  # +3 items, + log entry

    try:
        for i in range(1, 10):
            time.sleep(1)
            schedule.run_pending()  # +3 items
            if i == 3:
                raise KeyboardInterrupt  # 1+3 times through loop
    except KeyboardInterrupt:
        log.info("keyboard press -> exiting gracefully")

    assert len(engine.queue) == 12, f"{engine.queue=}"
