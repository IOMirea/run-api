import logging

import asyncpg

from aiohttp import web

log = logging.getLogger(__name__)


async def on_startup(app: web.Application) -> None:
    log.debug("creating postgres connection")
    app["pg"] = await asyncpg.create_pool(**app["config"]["postgresql"])


async def on_cleanup(app: web.Application) -> None:
    log.debug("closing postgres connection")
    await app["pg"].close()


def setup(app: web.Application) -> None:
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)
