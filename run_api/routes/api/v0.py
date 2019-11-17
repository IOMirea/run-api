import json
import time
import logging

from json import JSONDecodeError
from typing import Any, Dict, List

from aiohttp import ClientSession, web

from ...utils import validate_language, get_query_bool_flag
from ...constants import SUPPORTED_LANGUAGES

routes = web.RouteTableDef()


log = logging.getLogger(__name__)


@routes.get(r"/languages/{language_code}")
async def get_language(req: web.Request) -> web.Response:
    language = validate_language(req.match_info["language_code"])

    return web.json_response(language.to_json())


@routes.get(r"/languages")
async def get_languages(req: web.Request) -> web.Response:
    unique_langs = set(SUPPORTED_LANGUAGES.values())

    return web.json_response([l.to_json() for l in unique_langs])


@routes.post(r"/languages/{language_name}")
async def run_code(req: web.Request) -> web.Response:
    start_time = time.time()

    language = validate_language(req.match_info["language_name"])

    body = await req.read()
    if not body:
        data: Dict[str, Any] = {}
    else:
        try:
            data = json.loads(body)
        except JSONDecodeError:
            raise web.HTTPBadRequest(reason="Bad json in body: unable to decode")

        if not isinstance(data, dict):
            raise web.HTTPBadRequest(reason="Bad json in body: root object is not map")

    payload = {"code": data.pop("code", language.example)}

    if language.compiled:
        compile_args = data.pop("compile_args", language.compile_args)
        payload["compile_command"] = f"{language.compiler} {compile_args}"

    payload["merge_output"] = get_query_bool_flag(req, "merge", False)

    backend_run_url = (
        f"{req.config_dict['config']['app']['run-lb-ip']}/run/{language.name}"
    )

    log.debug("sending request to %s", backend_run_url)

    async with ClientSession() as cs:
        async with cs.post(backend_run_url, json=payload) as resp:
            if resp.status != 200:
                log.error("bad response status: %d: %s", resp.status, resp.reason)

                raise web.HTTPInternalServerError(
                    reason=f"Backend response error: {resp.reason}"
                )

            try:
                response_json = await resp.json()
            except JSONDecodeError:
                log.error("bad json returned by backend: %s", await req.text())
                raise web.HTTPInternalServerError(
                    reason="Backend response decoding error"
                )

    return web.json_response(
        {"processing_time": time.time() - start_time, **response_json}
    )


@routes.get(r"/sessions/{session_id:(\w|\d)+}")
async def get_session(req: web.Request) -> web.Response:
    session_id = req.match_info["session_id"]

    # TODO

    return web.json_response(dict(message=f"Session {session_id} ws connection. TODO"))


@routes.delete(r"/sessions/{session_id:(\w|\d)+}")
async def kill_session(req: web.Request) -> web.Response:
    session_id = req.match_info["session_id"]

    # TODO

    return web.json_response(dict(message=f"Killed session {session_id}"))


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
