from __future__ import annotations

from pathlib import Path

from typed_settings import load_settings, option, settings

from installer.settings import LOADER

FILE_SYSTEM_ROOT = Path("/")


##


@settings
class ShellConfigSettings:
    etc: bool = option(
        default=False,
        help="Set up in '/etc/profile.d/*.sh' instead of '~/.{bash,zsh}rc'",
    )


SHELL_CONFIG_SETTINGS = load_settings(ShellConfigSettings, [LOADER])


##


@settings
class SSHDSettings:
    permit_root_login: bool = option(default=False, help="Permit root login")


SSHD_SETTINGS = load_settings(SSHDSettings, [LOADER])


__all__ = [
    "FILE_SYSTEM_ROOT",
    "SHELL_CONFIG_SETTINGS",
    "SSHD_SETTINGS",
    "SSHDSettings",
    "ShellConfigSettings",
]
