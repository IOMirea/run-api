import asyncio
import logging

from typing import Callable, Awaitable

from aiohttp import web

log = logging.getLogger(__name__)

HandlerType = Callable[[web.Request], Awaitable[web.Response]]


@web.middleware
async def error_handler(req: web.Request, handler: HandlerType) -> web.Response:
    try:
        return await handler(req)
    except (web.HTTPSuccessful, web.HTTPRedirection):
        raise
    except web.HTTPException as e:
        status = e.status
        message = e.text
    except asyncio.CancelledError:
        if req.config_dict["args"].debug:
            raise

        status = 500
        message = f"{status} Internal server error"
    except Exception as e:
        log.exception("Error handling request", exc_info=e, extra={"request": req})
        status = 500
        message = f"{status}: Internal server error"

    # TODO: unique codes
    return web.json_response({"message": message}, status=status)
