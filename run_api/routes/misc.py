import os

from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/")
async def index(req: web.Request) -> web.Response:
    return web.Response(body=f"run-api {os.environ['GIT_COMMIT']}")
