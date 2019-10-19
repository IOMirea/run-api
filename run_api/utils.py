from aiohttp import web

from .constants import SUPPORTED_LANGUAGES, SUPPORTED_LANGUAGES_NAME_MAP
from .types.language import Language


def validate_language(string: str) -> Language:
    if string.isdigit():
        try:
            integer = int(string)
        except MemoryError:  # should not happen normally
            raise web.HTTPBadRequest(reason="Language code is not a valid integer")

        language = SUPPORTED_LANGUAGES.get(integer)
        if language is None:
            raise web.HTTPBadRequest(reason="Not a valid language code")

        return language

    string = string.lower()
    language_code = SUPPORTED_LANGUAGES_NAME_MAP.get(string)

    if language_code is not None:
        return language_code

    raise web.HTTPBadRequest(reason="Not a valid language alias")
