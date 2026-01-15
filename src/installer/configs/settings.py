from __future__ import annotations

from pathlib import Path

from typed_settings import load_settings, option, settings

from installer.settings import LOADER


@settings
class RootSettings:
    root: Path = option(default=Path("/"), help="File system root")


ROOT_SETTINGS = load_settings(RootSettings, [LOADER])


##


@settings
class SSHDSettings:
    permit_root_login: bool = option(default=False, help="Permit root login")


SSHD_SETTINGS = load_settings(SSHDSettings, [LOADER])


__all__ = ["ROOT_SETTINGS", "SSHD_SETTINGS", "RootSettings", "SSHDSettings"]
