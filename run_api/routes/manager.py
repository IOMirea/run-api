import os
import re
import signal

from json import JSONDecodeError
from logging import getLogger

from aiohttp import ClientSession, web
from aiohttp.client_exceptions import InvalidURL

from ..rpc import COMMAND_UPDATE_RUNNERS, COMMAND_UPDATE_LANGUAGE

log = getLogger(__name__)

ORG_NAME = "iomirea"

API_REPO_NAME = f"{ORG_NAME}/run-api-public"
RUNNER_REPO_NAME = f"{ORG_NAME}/run-api-private"

LANG_REPO_PATTERN = re.compile(f"{ORG_NAME}/run-lang-(.+)")


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
        log.debug("killing process")

        os.kill(os.getpid(), signal.SIGTERM)

    elif repository == RUNNER_REPO_NAME:
        await req.config_dict["rpc"].call(COMMAND_UPDATE_RUNNERS)

    else:
        match = LANG_REPO_PATTERN.fullmatch(repository)
        if match is not None:
            await req.config_dict["rpc"].call(
                COMMAND_UPDATE_LANGUAGE, dict(language=match[1])
            )

    return web.Response()
