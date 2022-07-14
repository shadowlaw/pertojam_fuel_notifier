import os
from distutils.util import strtobool

from dotenv import load_dotenv
import logging.config
from os import getenv

from custom_logging.handler.TelegramMessageHandler import TelegramMessageHandler

load_dotenv(dotenv_path='app_env/.env')

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
        },
        "admin_alert": {
            "class": "custom_logging.handler.TelegramMessageHandler.TelegramMessageHandler",
            "level": getenv("LOGGER_ADMIN_ALERT_HANDLER_LOG_LEVEL"),
            "formatter": "default",
            "bot_token": getenv("TELEGRAM_TOKEN"),
            "chat_id": getenv("TELEGRAM_ADMIN_CHAT_ID")
        }
    },
    "root": {
        "level": getenv("LOGGER_ROOT_LOG_LEVEL"),
        "handlers": ["console", "admin_alert"]
    }
}

APP = {
    "FUEL_URL": os.getenv("FUEL_URL"),
    "FUEL_TABLE_PATH": os.getenv("FUEL_TABLE_PATH"),
    "SELENIUM_IS_REMOTE": bool(strtobool(os.getenv('SELENIUM_IS_REMOTE'))),
    "SELENIUM_REMOTE_URL": os.getenv('SELENIUM_REMOTE_URL'),
    "SELENIUM_HEADLESS": bool(strtobool(os.getenv("SELENIUM_HEADLESS"))),
    "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN"),
    "TELEGRAM_GROUP_ID": os.getenv("TELEGRAM_GROUP_ID"),
}

logging.config.dictConfig(LOGGING_CONFIG)
