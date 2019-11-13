from __future__ import annotations

from typing import Any, List, Optional


class Language:

    __slots__ = ("name", "aliases", "active", "example", "compile_args")

    def __init__(
        self,
        *,
        name: str,
        aliases: List[str],
        active: bool,
        example: str,
        compile_args: Optional[str] = None,
    ):
        self.name = name
        self.aliases = aliases
        self.active = active
        self.example = example
        self.compile_args = compile_args

    @classmethod
    def from_json(cls, data: Any) -> Language:
        return cls(
            name=data["name"],
            aliases=data["aliases"],
            active=data.get("active", True),
            example=data["example"],
            compile_args=data.get("compile_args"),
        )

    def to_json(self) -> Any:
        result = {}
        for property in ("name", "aliases", "example", "compiled"):
            result[property] = getattr(self, property)

        if self.compiled:
            result["compile_args"] = self.compile_args

        return result

    @property
    def compiled(self) -> bool:
        return self.compile_args is not None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name} active={self.active}>"
