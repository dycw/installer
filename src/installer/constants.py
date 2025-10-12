from __future__ import annotations

from pathlib import Path

HOME = Path("~").expanduser()
XDG_CONFIG_HOME = HOME / ".config"
LOCAL_BIN = HOME / ".local/bin"
SSH = HOME / ".ssh"


__all__ = ["HOME", "LOCAL_BIN", "SSH", "XDG_CONFIG_HOME"]
