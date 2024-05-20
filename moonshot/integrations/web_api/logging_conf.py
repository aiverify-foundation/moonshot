import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Literal

from dependency_injector import providers

from .types.types import UvicornLoggingConfig

COLORS = {
    "HEADER": "\033[95m",
    "OKBLUE": "\033[94m",
    "OKGREEN": "\033[92m",
    "WARNING": "\033[93m",
    "FAIL": "\033[91m",
    "ENDC": "\033[0m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
    "WHITE": "\033[97m",
}


class ColorizedFormatter(logging.Formatter):
    LEVEL_COLORS = {
        logging.DEBUG: COLORS["OKBLUE"],
        logging.INFO: COLORS["OKGREEN"],
        logging.WARNING: COLORS["WARNING"],
        logging.ERROR: COLORS["FAIL"],
        logging.CRITICAL: COLORS["HEADER"],
    }

    def __init__(
        self,
        fmt: str,
        datefmt: str | None = None,
        style: Literal["%"] = "%",
        disableColor: bool = False,
    ):
        super().__init__(fmt, datefmt, style)
        self.disableColor = disableColor

    def format(self, record: logging.LogRecord):
        if self.disableColor:
            return super().format(record)
        else:
            color = str(self.LEVEL_COLORS.get(record.levelno))
            message = super().format(record)
            return color + message + COLORS["ENDC"]


def create_logging_dir(log_file_path: str):
    if not os.path.exists(log_file_path):
        os.makedirs(log_file_path)


def configure_app_logging(cfg: providers.Configuration):
    if cfg.log.logging():
        create_logging_dir(cfg.log.log_file_path())

    file_handler = RotatingFileHandler(
        filename=cfg.log.log_file_path() + "/web_api.log",
        maxBytes=cfg.log.log_file_max_size(),
        backupCount=cfg.log.log_file_backup_count(),
    )
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(ColorizedFormatter(cfg.log.format()))

    logging.basicConfig(
        handlers=[file_handler, stream_handler],
        level=cfg.log.level(),
        format=cfg.log.format(),
    )

    logging.info("Logging is configured.")


def create_uvicorn_log_config(cfg: providers.Configuration) -> UvicornLoggingConfig:
    if cfg.log.logging():
        create_logging_dir(cfg.log.log_file_path())

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "moonshot.integrations.web_api.logging_conf.ColorizedFormatter",
                "format": cfg.log.format(),
            },
            "file_formatter": {
                "()": "moonshot.integrations.web_api.logging_conf.ColorizedFormatter",
                "format": cfg.log.format(),
                "disableColor": True,
            },
        },
        "handlers": {
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": cfg.log.log_file_path() + "/web_api.log",
                "maxBytes": cfg.log.log_file_max_size(),
                "backupCount": cfg.log.log_file_backup_count(),
                "formatter": "file_formatter",
            },
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
        },
        "root": {
            "level": cfg.log.level(),
            "handlers": ["file", "console"],
        },
    }
