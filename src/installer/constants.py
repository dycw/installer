from __future__ import annotations

from pathlib import Path

HOME = Path("~").expanduser()
LOCAL_BIN = HOME / ".local/bin"
SSH = HOME / ".ssh"
XDG_CONFIG_HOME = HOME / ".config"


__all__ = ["HOME", "LOCAL_BIN", "SSH", "XDG_CONFIG_HOME"]
