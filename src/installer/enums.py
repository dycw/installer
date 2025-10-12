from __future__ import annotations

from enum import Enum, auto
from platform import system


class System(Enum):
    mac = auto()
    linux = auto()

    @classmethod
    def identify(cls) -> System:
        match system():
            case "Darwin":
                return System.mac
            case "Linux":
                return System.linux
            case _system:
                msg = f"Invalid system: {_system!r}"
                raise TypeError(msg)


__all__ = ["System"]
