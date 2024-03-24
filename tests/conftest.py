from typing import Callable
import random
import string

import pytest


def pytest_sessionfinish(session, exitstatus):
    """
    After tests are run clean up ./tests/data/ folder
    by deleting all *-temp.db files
    """
    import os

    for file in os.listdir("./tests/test_data/"):
        if file.endswith("-temp.db"):
            os.remove("./tests/test_data/" + file)


def pytest_addoption(parser):
    parser.addoption(
        "--outside",
        action="store_true",
        dest="outside",
        default=False,
        help="(custom) enable outside requests",
    )
    parser.addoption(
        "--longtest",
        action="store_true",
        dest="longtest",
        default=False,
        help="(custom) enable long tests",
    )

@pytest.fixture(scope="session")
def temp_tinyflux_path():
    r = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))

    class Config:
        TINYFLUX_PATH = f"./tests/test_data/{r}-temp.db"

    return Config

@pytest.fixture(scope="session")
def mock_log() -> Callable[[str], object]:  # logging.Logger
    def return_none(*args, **kwargs):
        """Ignores all arguments and returns None."""
        print(args, kwargs)

    class MockLog(object):
        def __init__(self, *args, **kwargs):
            pass

        def __getattr__(self, attrname):
            """
            Handles lookups of attributes that aren't
            found through the normal lookup - all of them.
            """
            return return_none

    return MockLog


@pytest.fixture(scope="session")
def mock_app_engine() -> Callable[[str], object]:  # Engine
    class MockAppEngine(object):
        def __init__(self, log, *args, **kwargs):
            self.log = log()
            self.queue = []

        def insert(self, *args, **kwargs):
            self.log.info(f"Added to engine {(args, kwargs)}")
            self.queue.append((args, kwargs))
            print(args, kwargs)

        def __getattr__(self, attrname):
            """
            Handles lookups of attributes that aren't
            found through the normal lookup - all of them.
            """
            return None

    return MockAppEngine


@pytest.fixture(scope="session")
def mock_bom() -> Callable[[str], object]:  # Engine
    class MockBOM(object):
        def __init__(self, log, *args, **kwargs):
            self.log = log()

        def get_points(self, *args, **kwargs):
            result = [
                {"random BOM point1": "random value1"},
                {"random BOM point2": "random value2"},
            ]
            self.log.critical(f"Extracted by BOM {result}")
            return result

        def __getattr__(self, attrname):
            """
            Handles lookups of attributes that aren't
            found through the normal lookup - all of them.
            """
            raise NotImplementedError

    return MockBOM


@pytest.fixture(scope="session")
def mock_p110() -> Callable[[str], object]:  # Engine
    class MockP110(object):
        def __init__(self, log, *args, **kwargs):
            self.log = log()

        def get_point(self, *args, **kwargs):
            result = {"random P110 point1": "random value1"}
            self.log.error(f"Extracted by P110 {result}")
            return result

        def __getattr__(self, attrname):
            """
            Handles lookups of attributes that aren't
            found through the normal lookup - all of them.
            """
            raise NotImplementedError

    return MockP110
