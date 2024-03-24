import time

import schedule

from timeseries_etl.app import bom_job, p110_job


def test_app(mock_app_engine, mock_bom, mock_p110, mock_log):
    app_log = mock_log()
    engine = mock_app_engine(mock_log)

    schedule.every(1).seconds.do(
        bom_job, bom_service=mock_bom(mock_log), engine_service=engine
    )
    schedule.every(1).seconds.do(
        p110_job, p110_service=mock_p110(mock_log), engine_service=engine
    )
    schedule.run_all()  # +3 items, + log entry

    try:
        for i in range(1, 10):
            time.sleep(1)
            schedule.run_pending()  # +3 items
            if i == 3:
                raise KeyboardInterrupt  # 1+3 times through loop
    except KeyboardInterrupt:
        app_log.info("keyboard press -> exiting gracefully")

    assert len(engine.queue) == 12, f"{engine.queue=}"
