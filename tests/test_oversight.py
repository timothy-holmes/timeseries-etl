import os.path
from datetime import datetime

from timeseries_etl.oversight import configured_logger, config


def patch_log():  # not thread-safe
    name = "test_log"
    log_file = "./tests/test_data/logs/{name}.log".format(name=name)

    # get existing log file
    if os.path.isfile(log_file):
        with open(log_file, "r") as f:
            old_contents = f.readlines()
    else:
        old_contents = []

    yield old_contents

    # create new logger
    yield configured_logger(name)

    # get new contents
    if os.path.isfile(log_file):
        with open(log_file, "r") as f:
            new_contents = f.readlines()
    else:
        new_contents = []

    yield new_contents


def test_logging():
    log_contents_comparator = patch_log()  # not thread-safe

    old_log_contents = next(log_contents_comparator)
    old_hellos = [entry.split(" | ")[-1].strip() for entry in old_log_contents]

    log = next(log_contents_comparator)
    log.info("hello")
    log.debug("hello")
    log.warning("hello")
    log.error("hello")
    log.critical("hello")

    new_log_contents = next(log_contents_comparator)
    new_hellos = [entry.split(" | ")[-1].strip() for entry in new_log_contents]

    assert new_hellos == old_hellos + ["hello"] * 5, f'{len(new_hellos)=}, {len(old_hellos)=}'
