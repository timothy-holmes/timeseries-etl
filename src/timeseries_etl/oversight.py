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
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "precise",
            "level": "DEBUG",
            "filename": "./logs/{name}.log",
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


def configured_logger(name: str) -> logging.Logger:
    logging.getLogger('not_root')
    logging.name = name
    
    h = config.get('handlers', {}).get('file', {}).copy()
    h['filename'] = h['filename'].format(name=name)
    logging.addHandler(
        logging.handlers.TimedRotatingFileHandler(
            **h
        )
    )

    return logging.getLogger(name)
