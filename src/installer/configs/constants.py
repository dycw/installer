from __future__ import annotations

from pathlib import Path

RELATIVE_HOME = Path.home().relative_to("/")


__all__ = ["RELATIVE_HOME"]
