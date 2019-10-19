from __future__ import annotations

from typing import Any, List


class Language:

    __slots__ = ("code", "active", "aliases", "example")

    def __init__(self, *, code: int, active: bool, aliases: List[str], example: str):
        self.code = code
        self.active = active
        self.aliases = aliases
        self.example = example

    @classmethod
    def from_json(cls, data: Any) -> Language:
        return cls(
            code=data[0],
            active=data[1].get("active", True),
            aliases=data[1]["aliases"],
            example=data[1]["example"],
        )

    @property
    def name(self) -> str:
        return self.aliases[0]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} code={self.code} aliases={self.aliases}>"
