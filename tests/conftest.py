def pytest_sessionfinish(session, exitstatus):
    """
    After tests are run clean up ./tests/data/ folder 
    by deleting all *-temp.db files
    """
    import os

    for file in os.listdir("./tests/data/"):
        if file.endswith("-temp.db"):
            os.remove("./tests/data/" + file)
