from __future__ import annotations

from typed_settings import load_settings, option, settings

from installer.utilities import LOADER


@settings
class SudoSettings:
    sudo: bool = option(default=False, help="Run as 'sudo'")


SUDO_SETTINGS = load_settings(SudoSettings, [LOADER])


__all__ = ["SUDO_SETTINGS", "SudoSettings"]
