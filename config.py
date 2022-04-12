from dotenv import load_dotenv
import logging.config
from os import getenv

load_dotenv()

LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "class": "logging.Formatter",
            "format": getenv("LOGGER_DEFAULT_FORMAT")
        }
    },
    "handlers": {
        "console": {
            "level": getenv("LOGGER_CONSOLE_HANDLER_LOG_LEVEL"),
            "class": "logging.StreamHandler",
            "formatter": "default"
        }
    },
    "root": {
        "level": getenv("LOGGER_ROOT_LOG_LEVEL"),
        "handlers": ["console"]
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
