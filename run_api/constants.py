import os

from typing import Dict

import yaml

from .types.language import Language

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.sep.join((BASE_DIR, "data"))

LANGUAGES_FILE = os.sep.join((DATA_DIR, "languages.yaml"))

# TODO: get language list dynamically from internal API
SUPPORTED_LANGUAGES: Dict[int, Language] = {}
SUPPORTED_LANGUAGES_NAME_MAP: Dict[str, Language] = {}


def read_languages() -> None:
    """Reads languages from file."""

    global SUPPORTED_LANGUAGES, SUPPORTED_LANGUAGES_NAME_MAP

    SUPPORTED_LANGUAGES = {}
    SUPPORTED_LANGUAGES_NAME_MAP = {}

    with open(LANGUAGES_FILE, "r") as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)

    if not isinstance(data, dict):
        raise ValueError("Bad yaml file: not a mapping")

    for i in data.items():
        language = Language.from_json(i)
        if not language.active:
            continue

        SUPPORTED_LANGUAGES[language.code] = language

        for alias in language.aliases:
            existing = SUPPORTED_LANGUAGES_NAME_MAP.get(alias)
            if existing is not None:
                raise ValueError(
                    f"Duplicate language alias: {alias}. Used in {existing}"
                )

            SUPPORTED_LANGUAGES_NAME_MAP[alias] = language


read_languages()
