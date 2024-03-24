import logging
import logging.handlers

# import logging.config

config = {
    "version": 1,
    "formatters": {
        "brief": {
            "format": " | ".join(
                [
                    "%(asctime)s",
                    "%(levelname)s",
                    "%(filename)s:%(lineno)d",
                    "%(message)s",
                ]
            ),
            "datefmt": "%Y%m%d-%H%M%S",
            "style": "%",
        },
        "precise": {
            "format": " | ".join(
                [
                    "%(asctime)s",
                    "%(relativeCreated)i",
                    "%(levelname)s",
                    "%(filename)s:%(lineno)d",
                    "%(funcName)s",
                    "%(message)s",
                ]
            ),
            "datefmt": "%Y%m%d-%H%M%S",
            "style": "%",
        },
        # "email": {
        #     "format": '\n'.join([
        #         'Entry time: {asctime}, ({relativeCreated:.0f} after logger start)',
        #         'Entry level: {levelname}',
        #         'Logger name, file, line: {name}, {filename}, {lineno}',
        #         'Function name: {funcName}',
        #         'Message: {message}','\n'
        #     ]),
        #     "datefmt": "%Y-%j-%H%M%S",
        #     "style": "{"
        # }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "brief",
            "level": "DEBUG",
            "filters": [],
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "precise",
            "level": "DEBUG",
            "filename": "./logs/{name}.log", # "./tests/test_data/logs/{name}.log",
            "when": "midnight",
            "backupCount": 7,
        },
        # "email": {
        #     "class": "email_handler.SSLEmailHandler",
        #     "formatter": "email",
        #     "level": "WARNING",
        #     "email_config": {
        #         "host": "timothyholmes.com.au",
        #         "port": 465,
        #         "username": "notifications@timothyholmes.com.au",
        #         "password": secrets['email_password'],
        #         "toaddrs": ["tim.a.holmes+app@gmail.com"],
        #         "timeout": 120
        #     },
        #     "logger_config": {
        #         "subject": "Logger Entry ({name}): {now}",
        #     }
        # },
    },
    "loggers": {
        "not_root": {
            "handlers": [
                "console",
                # "file",
                # "email"
            ],
            # parent level -> handler level hierarchy
            "level": "DEBUG",
        }
    },
    "root": {
        "handlers": [
            # "console",
            # "file",
            # "email"
        ],
        "level": "ERROR",
    },
}

# logging.config.dictConfig(config)


def configured_logger(name: str) -> logging.Logger:
    print(name)
    logger = logging.getLogger(name)
    logger.setLevel("DEBUG")
    logger.propagate = False

    h_dict = config.get("handlers", {}).get("file", {})
    if name.startswith('test_'):
        filename = h_dict["filename"].format(name=name)
    else:
        filename = "./tests/test_data/logs/{name}.log".format(name=name)
    h_obj = logging.handlers.TimedRotatingFileHandler(
        filename=filename,
        when=h_dict["when"],
        backupCount=h_dict["backupCount"],
        # encoding=h_dict.get('encoding', None),
        # delay=h_dict.get('delay', False),
        # utc=h_dict.get('utc', False),
        # atTime=h_dict.get('atTime', None),
    )

    f_dict = config.get("formatters", {}).get("precise", {}).copy()
    f_obj = logging.Formatter(
        fmt=f_dict.get("format", None),
        datefmt=f_dict.get("datefmt", None),
        style=f_dict.get("style", None),
        validate=True,
    )

    h_obj.setFormatter(f_obj)
    logger.addHandler(h_obj)

    return logger
