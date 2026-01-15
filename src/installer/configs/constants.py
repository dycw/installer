from __future__ import annotations

from pathlib import Path

AUTHORIZED_KEYS = "authorized_keys"
REL_HOME = Path.home().relative_to("/")
REL_SSH = REL_HOME / ".ssh"
SSH = ".ssh"


__all__ = ["AUTHORIZED_KEYS", "REL_HOME", "REL_SSH", "SSH"]
