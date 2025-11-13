from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

type PathLike = Path | str
type SSHSymlink = PathLike | tuple[PathLike, str]
type SSHTemplate = (
    tuple[PathLike, Mapping[str, Any]] | tuple[PathLike, Mapping[str, Any], str]
)


__all__ = ["PathLike", "SSHSymlink", "SSHTemplate"]
