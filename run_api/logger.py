# code originally taken from https://github.com/Tarakania/discord-bot

import logging.config

from .cli import args

LEVEL_TO_COLOR_VALUE = {
    "INFO": "32",  # green
    "WARNING": "33",  # yellow
    "ERROR": "31",  # red
    "CRITICAL": "41",  # white on red
}

COLOR_START = "\033["
COLOR_RESET = "\033[0m"

VERBOSE_FORMAT = "%(asctime)s %(levelname)-8s %(name)s %(message)s"
SIMPLE_FORMAT = "%(levelname)-8s %(name)s %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        formatted = super().format(record)

        color_value = LEVEL_TO_COLOR_VALUE.get(record.levelname)
        if color_value is None:
            return formatted

        return f"{COLOR_START}{color_value}m{formatted}{COLOR_RESET}"


def test_logger() -> None:
    print("----- Start logger test -----")

    message = "The quick brown fox jumps over the lazy dog"

    for level in (
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    ):
        logging.log(level, message)

    print("----- End logger test -------")


def logging_name_to_level(string: str) -> int:
    logging_level = logging.getLevelName(string.upper())

    if isinstance(logging_level, int):
        return logging_level

    raise ValueError(f"Unknown logging level passed: {logging_level}")


def setup_logger() -> None:
    LOGGING_CONFIG = {
        "version": 1,
        "formatters": {
            "verbose": {"format": VERBOSE_FORMAT, "datefmt": DATE_FORMAT},
            "simple": {"format": SIMPLE_FORMAT},
            "colorful_verbose": {
                "()": ColorFormatter,
                "format": VERBOSE_FORMAT,
                "datefmt": DATE_FORMAT,
            },
            "colorful_simple": {"()": ColorFormatter, "format": SIMPLE_FORMAT},
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
            "colorful_console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "colorful_simple",
            },
        },
        "loggers": {
            "asyncio": {
                "level": "WARNING",
                "handlers": ["console"],
                "propagate": False,
            },
            "aiohttp": {
                "level": "WARNING",
                "handlers": ["console"],
                "propagate": False,
            },
            "sentry_sdk": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": False,
            },
            "aioredis": {
                "level": "WARNING",
                "handlers": ["console"],
                "propagate": False,
            },
        },
        "root": {
            "level": logging_name_to_level(args.verbosity),
            "handlers": ["console" if args.no_colors else "colorful_console"],
        },
        "disable_existing_loggers": False,
    }

    logging.config.dictConfig(LOGGING_CONFIG)

    if args.test_logger:
        test_logger()
