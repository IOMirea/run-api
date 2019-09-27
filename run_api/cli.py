# code originally taken from https://github.com/Tarakania/discord-bot

import os
import logging
import argparse

from pathlib import Path

from .constants import DATA_DIR

DEFAULT_PORT = "8080"
DEFAULT_HOST = "0.0.0.0"
DEFAULT_CONFIG_PATH = os.sep.join((DATA_DIR, "config.yaml"))

argparser = argparse.ArgumentParser(
    prog="run_api", description="Tarakania RPG discord bot"
)
argparser.add_argument(
    "--host",
    default=DEFAULT_HOST,
    help=f"Host to run API on. Defaults to {DEFAULT_HOST}",
)
argparser.add_argument(
    "--port",
    default=DEFAULT_PORT,
    help=f"Port to run update webhook on. Defaults to {DEFAULT_PORT}",
)
argparser.add_argument(
    "--config-file",
    type=Path,
    default=Path(DEFAULT_CONFIG_PATH),
    help=f"Path to the config file. Defaults to {DEFAULT_CONFIG_PATH}",
)
argparser.add_argument(
    "--enable-updater", action="store_true", help="Enables updater. Disabled by default"
)
argparser.add_argument(
    "--enable-sentry", action="store_true", help="Enables sentry. Disabled by default"
)


def _convert_logging_verbosity(string: str) -> int:
    logging_level = logging.getLevelName(string.upper())

    if isinstance(logging_level, int):
        return logging_level

    raise ValueError(f"Unknown logging level passed: {logging_level}")


argparser.add_argument(
    "--verbosity",
    "-v",
    choices=["critical", "error", "warning", "info", "debug"],
    default="info",
    help="Verbosity level",
)

argparser.add_argument(
    "--no-colors", action="store_true", help="Disables console colors"
)

argparser.add_argument("--test-logger", action="store_true", help="Perform logger test")

args = argparser.parse_args()
args.verbosity = _convert_logging_verbosity(args.verbosity)
