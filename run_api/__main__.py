import logging

from typing import Any, Dict

import uvloop
import sentry_sdk

from aiohttp import web
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

# from .rpc import setup_rpc
from .cli import args
from .db.pg import setup as setup_pg
from .config import read_config
from .logger import setup_logger
from .middlewares import error_handler
from .routes.api.v0 import routes as api_v0_routes
from .routes.manager import routes as manager_routes

DEBUG_MODE = args.verbosity == logging.DEBUG


def create_app(config: Dict[str, Any]) -> web.Application:
    base_app = web.Application()
    base_app["config"] = config

    base_app.add_routes(manager_routes)

    base_app.middlewares.append(error_handler)

    setup_pg(base_app)
    # setup_rpc(base_app)

    base_api_app = web.Application()

    api_v0_app = web.Application()
    api_v0_app.add_routes(api_v0_routes)

    base_api_app.add_subapp("/v0", api_v0_app)
    base_app.add_subapp("/api", base_api_app)

    return base_app


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

    uvloop.install()

    app = create_app(config)
    web.run_app(app, host=args.host, port=args.port)
