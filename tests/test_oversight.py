import os.path

from timeseries_etl.oversight import configured_logger, config


def patch_log():  # not thread-safe
    log_file = (
        config.get("handlers", {})
        .get("file", {})
        .get("filename")
        .format(name="test_log")
    )

    og_contents = []
    new_contents = []

    # save existing log file
    if os.path.isfile(log_file):
        og_contents = open(log_file, "r").readlines()
    yield configured_logger("test_log")

    # get new contents
    if os.path.isfile(log_file):
        new_contents = open(log_file, "r").readlines()

    # return original contents
    if os.path.isfile(log_file):
        open(log_file, "w").writelines(og_contents)
    yield new_contents


def test_logging():
    log_contents = patch_log()  # not thread-safe
    log = next(log_contents)

    log.info("hello")
    log.debug("hello")
    log.warning("hello")
    log.error("hello")
    log.critical("hello")

    log_contents = next(log_contents)
    hellos = [entry.split(" | ")[-1].strip() for entry in log_contents]

    assert hellos == ["hello"] * 5
