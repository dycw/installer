from __future__ import annotations

from pathlib import Path

HOME = Path("~").expanduser()


LOCAL_BIN = HOME / ".local/bin"
SSH = HOME / ".ssh"
XDG_CONFIG_HOME = HOME / ".config"


AUTHORIZED_KEYS = SSH / "authorized_keys"
KNOWN_HOSTS = SSH / "known_hosts"
SSH_CONFIG = SSH / "config"


__all__ = [
    "AUTHORIZED_KEYS",
    "HOME",
    "KNOWN_HOSTS",
    "LOCAL_BIN",
    "SSH",
    "SSH_CONFIG",
    "XDG_CONFIG_HOME",
]
