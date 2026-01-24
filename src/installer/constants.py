from __future__ import annotations

from pathlib import Path

from utilities.constants import HOME

FILE_SYSTEM_ROOT = Path("/")
RELATIVE_HOME = HOME.relative_to("/")


__all__ = ["FILE_SYSTEM_ROOT", "RELATIVE_HOME"]
