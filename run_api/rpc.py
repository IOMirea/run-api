import asyncio
import logging

from copy import copy

from jarpc import Client
from aiohttp import web

log = logging.getLogger(__name__)

COMMAND_UPDATE_RUNNERS = 0


async def on_startup(app: web.Application) -> None:
    config = copy(app["config"]["redis-rpc"])

    host = config.pop("host")
    port = config.pop("port")

    log.debug("creating rpc connection")

    app["rpc"] = Client("run-api")
    asyncio.create_task(app["rpc"].start((host, port), **config))


async def on_cleanup(app: web.Application) -> None:
    log.debug("closing rpc connection")
    app["rpc"].close()


def setup(app: web.Application) -> None:
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
