
import logging
from logging.handlers import RotatingFileHandler
import sys
import yaml


COLORS = {
    "HEADER": "\033[95m",
    "OKBLUE": "\033[94m",
    "OKGREEN": "\033[92m",
    "WARNING": "\033[93m",
    "FAIL": "\033[91m",
    "ENDC": "\033[0m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
}

class ColorizedFormatter(logging.Formatter):
    LEVEL_COLORS = {
        logging.DEBUG: COLORS["OKBLUE"],
        logging.INFO: COLORS["OKGREEN"],
        logging.WARNING: COLORS["WARNING"],
        logging.ERROR: COLORS["FAIL"],
        logging.CRITICAL: COLORS["HEADER"],
    }

    def format(self, record: logging.LogRecord):
        color = str(self.LEVEL_COLORS.get(record.levelno))
        message = super().format(record)
        return color + message + COLORS["ENDC"]


def configure_logging():
    with open("web_api/config.yml", "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    file_handler = RotatingFileHandler(
        filename=cfg['log']['log_file_path'],
        maxBytes=cfg['log']['log_file_max_size'],
        backupCount=cfg['log']['log_file_backup_count']
    )
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(ColorizedFormatter(cfg['log']['format']))

    logging.basicConfig(
        handlers=[file_handler, stream_handler],
        level=cfg['log']['level'],
        format=cfg['log']['format'],
    )

    logging.info("Logging is configured.")