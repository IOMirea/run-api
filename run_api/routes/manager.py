import os
import signal

from json import JSONDecodeError
from logging import getLogger

from aiohttp import ClientSession, web
from aiohttp.client_exceptions import InvalidURL

from ..rpc import COMMAND_UPDATE_RUNNERS
from ..utils import run_shell_command

log = getLogger(__name__)

API_REPO_NAME = "iomirea/run-api-public"
RUNNER_REPO_NAME = "iomirea/run-api-private"


async def docker_hub_webhook(req: web.Request) -> web.Response:
    try:
        data = await req.json()
    except JSONDecodeError:
        raise web.HTTPBadRequest(reason="Bad json")

    try:
        callback_url = data["callback_url"]
    except KeyError:
        raise web.HTTPBadRequest(reason="callback_url key is missing")

    try:
        repository = data["repository"]["repo_name"]
    except KeyError:
        raise web.HTTPBadRequest(reason="repository name is missing")

    if not isinstance(callback_url, str):
        raise web.HTTPBadRequest(reason="callback_url is not string")

    async with ClientSession() as cs:
        try:
            async with cs.post(
                callback_url, json=dict(state="success", context="IOMirea run API")
            ) as resp:
                if not resp.status == 200:
                    log.error("error sending response to docker hub: %s", str(resp))
        except InvalidURL:
            raise web.HTTPBadRequest(reason="bad callback_url url")

    if repository == API_REPO_NAME:
        await run_shell_command(f"docker pull {API_REPO_NAME}", wait=True)

        os.kill(os.getpid(), signal.SIGTERM)

    elif repository == RUNNER_REPO_NAME:
        await req["rpc"].call(COMMAND_UPDATE_RUNNERS)

    return web.Response()
