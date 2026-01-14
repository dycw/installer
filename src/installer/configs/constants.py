from __future__ import annotations

from pathlib import Path

REL_HOME = Path.home().relative_to("/")
REL_SSH = REL_HOME / ".ssh"


__all__ = ["REL_HOME", "REL_SSH"]
