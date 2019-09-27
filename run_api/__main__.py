import logging

import uvloop
import sentry_sdk

from aiohttp import web
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from .cli import args
from .config import read_config
from .logger import setup_logger

DEBUG_MODE = args.verbosity == logging.DEBUG

if __name__ == "__main__":
    config = read_config(args.config_file)

    setup_logger()

    log = logging.getLogger(__name__)

    if args.enable_sentry:
        log.debug("Initializing sentry")

        sentry_sdk.init(
            dsn=config["sentry"]["dsn"],
            integrations=[AioHttpIntegration()],
            debug=DEBUG_MODE,
        )
    else:
        log.debug("Skipping sentry initialization")

    app = web.Application()

    uvloop.install()

    web.run_app(app, host=args.host, port=args.port)
