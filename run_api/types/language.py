from __future__ import annotations

from typing import Any, List, Optional


class Language:

    __slots__ = ("name", "aliases", "active", "example", "compiler", "compile_args")

    def __init__(
        self,
        *,
        name: str,
        aliases: List[str],
        active: bool,
        example: str,
        compiler: str,
        compile_args: Optional[str] = None,
    ):
        self.name = name
        self.aliases = aliases
        self.active = active
        self.example = example
        self.compiler = compiler
        self.compile_args = compile_args

    @classmethod
    def from_json(cls, data: Any) -> Language:
        return cls(
            name=data["name"],
            aliases=data["aliases"],
            active=data.get("active", True),
            example=data["example"],
            compiler=data.get("compiler"),
            compile_args=data.get("compile_args"),
        )

    def to_json(self) -> Any:
        result = {}
        for property in ("name", "aliases", "example", "compiled", "compile_args"):
            result[property] = getattr(self, property)

        return result

    @property
    def compiled(self) -> bool:
        return self.compiler is not None and self.compile_args is not None

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name} active={self.active}>"
