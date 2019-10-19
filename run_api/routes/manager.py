from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/docker-hub-webhook")
async def docker_hub_webhook(req: web.Request) -> web.Response:
    return web.Response(status=418)
