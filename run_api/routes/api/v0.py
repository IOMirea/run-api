import json
import time

from typing import Dict, List

from aiohttp import web

from ...utils import validate_language
from ...constants import SUPPORTED_LANGUAGES

routes = web.RouteTableDef()


@routes.post(r"/languages/{language_code}")
async def run_code(req: web.Request) -> web.Response:
    validate_language(req.match_info["language_code"])

    start_time = time.time()
    # internal API call
    execution_time = time.time() - start_time

    return web.json_response(
        dict(
            stdout="Code execution successfull\n",
            stderr="",
            execution_time=execution_time,
        )
    )


@routes.get(r"/languages/{language_code}")
async def get_language(req: web.Request) -> web.Response:
    language = validate_language(req.match_info["language_code"])

    return web.json_response(language.to_json())


@routes.get("/languages")
async def get_languages(req: web.Request) -> web.Response:
    return web.json_response([l.to_json() for l in SUPPORTED_LANGUAGES.values()])


@routes.get("/endpoints")
async def get_endpoints(req: web.Request) -> web.Response:
    endpoints: Dict[str, List[str]] = {}

    for route in req.app.router.routes():
        method = route.method

        if route.resource is None:
            raise RuntimeError(f"No canonical url for resource {route.resource!r}")

        path = route.resource.canonical

        endpoints[path] = endpoints.get(path, []) + [method]

    return web.json_response(text=json.dumps(endpoints, indent=4, sort_keys=True))
