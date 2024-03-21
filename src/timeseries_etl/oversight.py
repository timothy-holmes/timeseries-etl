import logging
import logging.config

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
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "precise",
            "level": "DEBUG",
            "filename": "./logs/my-first-log.log",
            "maxBytes": 1024,
            "backupCount": 3,
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
        "app_logger": {
            "handlers": [
                "console",
                "file",
                # "email"
            ],
            "level": "DEBUG",  # parent level -> handler level hierarchy (logger is gatekeeper, but doesn't override)
        }
    },
    "root": {
        "handlers": [
            # "console",
            # "file",
            # "email"
        ],
        "level": "ERROR",  # parent level -> handler level hierarchy (logger is gatekeeper, but doesn't override)
    },
}

logging.config.dictConfig(config)
log = logging.getLogger("app_logger")
