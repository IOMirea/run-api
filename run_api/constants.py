import os

from typing import Dict

import yaml

from .types.language import Language

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.sep.join((BASE_DIR, "data"))

LANGUAGES_FILE = os.sep.join((DATA_DIR, "languages.yaml"))

SUPPORTED_LANGUAGES: Dict[str, Language] = {}


def read_languages() -> None:
    """Reads languages from file."""

    global SUPPORTED_LANGUAGES

    SUPPORTED_LANGUAGES = {}

    with open(LANGUAGES_FILE, "r") as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)

    if not isinstance(data, dict):
        raise ValueError("Bad yaml file: not a mapping")

    for name, body in data.items():
        language = Language.from_json({"name": name, **body})
        if not language.active:
            continue

        SUPPORTED_LANGUAGES[language.name] = language

        for alias in language.aliases:
            existing = SUPPORTED_LANGUAGES.get(alias)
            if existing is not None:
                raise ValueError(
                    f"Duplicate language alias: {alias}. Used in {existing}"
                )

            SUPPORTED_LANGUAGES[alias] = language


read_languages()
