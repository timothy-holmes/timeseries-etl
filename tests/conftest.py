from typing import Callable

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
def mock_log() -> Callable[[str], object]: #logging.Logger
    def return_none(*args, **kwargs):
        """Ignores all arguments and returns None."""
        return None

    class MyClass(object):
        def __getattr__(self, attrname):
            """Handles lookups of attributes that aren't found through the normal lookup."""
            return return_none

    return MyClass
