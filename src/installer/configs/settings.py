from __future__ import annotations

from typed_settings import load_settings, option, settings

from installer.utilities import LOADER


@settings
class SSHDSettings:
    permit_root_login: bool = option(default=False, help="Permit root login")


SSHD_SETTINGS = load_settings(SSHDSettings, [LOADER])


__all__ = ["SSHD_SETTINGS", "SSHDSettings"]
