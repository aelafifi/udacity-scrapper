from typing import Any


class ObjectDict(dict):
    def __getattribute__(self, name: str) -> Any:
        if name in self:
            return self[name]
        return super().__getattribute__(name)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} object>"


