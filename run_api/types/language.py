from __future__ import annotations

from typing import Any, List, Optional


class Language:

    __slots__ = ("code", "active", "aliases", "example", "compile_args")

    def __init__(
        self,
        *,
        code: int,
        active: bool,
        aliases: List[str],
        example: str,
        compile_args: Optional[str] = None,
    ):
        self.code = code
        self.active = active
        self.aliases = aliases
        self.example = example
        self.compile_args = compile_args

    @classmethod
    def from_json(cls, data: Any) -> Language:
        return cls(
            code=data[0],
            active=data[1].get("active", True),
            aliases=data[1]["aliases"],
            example=data[1]["example"],
            compile_args=data[1].get("compile_args"),
        )

    def to_json(self) -> Any:
        result = {}
        for property in ("name", "code", "aliases", "example", "compiled"):
            result[property] = getattr(self, property)

        if self.compiled:
            result["compile_args"] = self.compile_args

        return result

    @property
    def name(self) -> str:
        return self.aliases[0]

    @property
    def compiled(self) -> bool:
        return self.compile_args is not None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} code={self.code} aliases={self.aliases}>"
