import asyncio
import logging

from typing import Optional

from aiohttp import web

from .constants import SUPPORTED_LANGUAGES
from .types.language import Language

log = logging.getLogger(__name__)

TRUTHY = {"yes", "1", "true", "t", ""}
FALSY = {"no", "0", "false", "f"}


class ShellResult:
    def __init__(self, stdout: bytes, stderr: bytes, exit_code: int):
        self.stdout_bytes = stdout
        self.stderr_bytes = stderr

        self.exit_code = exit_code

        self._stdout: Optional[str] = None
        self._stderr: Optional[str] = None

    @property
    def stdout(self) -> str:
        if self._stdout is None:
            self._stdout = self.stdout_bytes.decode()

        return self._stdout

    @property
    def stderr(self) -> str:
        if self._stderr is None:
            self._stderr = self.stderr_bytes.decode()

        return self._stderr

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} stdout={self.stdout} stderr={self.stderr}>"


def validate_language(string: str) -> Language:
    # if string.isdigit():
    #     try:
    #         integer = int(string)
    #     except MemoryError:  # should not happen normally
    #         raise web.HTTPBadRequest(reason="Language code is not a valid integer")
    #
    #     language = SUPPORTED_LANGUAGES.get(integer)
    #     if language is None:
    #         raise web.HTTPBadRequest(reason="Not a valid language code")
    #
    #     return language

    string = string.lower()
    language_code = SUPPORTED_LANGUAGES.get(string)

    if language_code is not None:
        return language_code

    raise web.HTTPBadRequest(reason="Not a valid language alias")


async def run_shell_command(command: str, wait: bool = False) -> ShellResult:
    log.debug("running shell command: %s", command)

    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    if not wait:
        return ShellResult(b"", b"", -1)

    stdout, stderr = await process.communicate()

    return ShellResult(stdout, stderr, process.returncode)


def get_query_bool_flag(req: web.Request, name: str, default: bool) -> bool:
    value = req.query.get(name)
    if value is None:
        return default

    value = value.lower()

    if value in TRUTHY:
        return True

    if value in FALSY:
        return False

    return default
