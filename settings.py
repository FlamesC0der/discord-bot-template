import os
import datetime
import logging
from logging.config import dictConfig
from dotenv import load_dotenv


load_dotenv()

DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")


LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "\033[94m[%(asctime)s] %(levelname)-7s | %(module)-15s | %(message)s\033[0m"
        },
        "verbose_w": {
            "format": "\033[93m[%(asctime)s] %(levelname)-7s | %(module)-15s | %(message)s\033[0m"
        },
        "verbose_f": {
            "format": "[%(asctime)s] %(levelname)-7s | %(module)-15s | %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG", 
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "verbose_w",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": f"logs/{datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}.log",
            "mode": "w",
            "formatter": "verbose_f",
        },
    },
    "loggers": {
        "bot": {
            "handlers": ["console", "file"], 
            "level": "INFO", 
            "propagate": False
        },
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

dictConfig(LOGGING_CONFIG)