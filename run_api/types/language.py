from __future__ import annotations

from typing import Any, List


class Language:

    __slots__ = ("name", "aliases", "active", "example", "compilers", "compile_args")

    def __init__(
        self,
        *,
        name: str,
        aliases: List[str],
        active: bool,
        example: str,
        compilers: List[str],
        compile_args: List[str] = None,
    ):
        self.name = name
        self.aliases = aliases
        self.active = active
        self.example = example
        self.compilers = compilers
        self.compile_args = compile_args

    @classmethod
    def from_json(cls, data: Any) -> Language:
        compilers = data.get("compilers", [])
        if not isinstance(compilers, list):
            compilers = [compilers]

        compile_args = data.get("compile_args", [])
        if not isinstance(compile_args, list):
            compile_args = [compile_args]

        return cls(
            name=data["name"],
            aliases=data.get("aliases", []),
            active=data.get("active", True),
            example=data["example"],
            compilers=compilers,
            compile_args=compile_args,
        )

    def to_json(self) -> Any:
        result = {}

        properties = ["name", "aliases", "example", "compiled"]
        if self.compiled:
            properties.append("compilers")
            properties.append("compile_args")

        for property in properties:
            result[property] = getattr(self, property)

        return result

    @property
    def compiled(self) -> bool:
        return bool(self.compilers) and bool(self.compile_args)

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name} active={self.active} compiled={self.compiled}>"
