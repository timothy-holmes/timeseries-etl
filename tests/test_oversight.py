import os.path

from timeseries_etl.oversight import configured_logger, config


def patch_log():  # not thread-safe
    name = 'test_log'
    log_file = (
        config.get("handlers", {})
        .get("file", {})
        .get("filename")
        .format(name=name)
    )

    old_contents = []
    new_contents = []

    # save existing log file
    if os.path.isfile(log_file):
        old_contents = open(log_file, "r").readlines()
    yield configured_logger(name)

    # get new contents
    if os.path.isfile(log_file):
        new_contents = open(log_file, "r").readlines()

    yield old_contents
    yield new_contents


def test_logging():
    log_contents = patch_log()  # not thread-safe
    log = next(log_contents)

    log.info("hello")
    log.debug("hello")
    log.warning("hello")
    log.error("hello")
    log.critical("hello")

    old_log_contents = next(log_contents)
    new_log_contents = next(log_contents)
    old_hellos = [entry.split(" | ")[-1].strip() for entry in old_log_contents]
    new_hellos = [entry.split(" | ")[-1].strip() for entry in new_log_contents]

    assert new_hellos == old_hellos + ["hello"] * 5
