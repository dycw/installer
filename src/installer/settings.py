from __future__ import annotations

from typed_settings import EnvLoader, load_settings, option, settings

LOADER = EnvLoader("")


##


@settings
class BatchSettings:
    batch_mode: bool = option(default=True, help="SSH batch mode")


BATCH_SETTINGS = load_settings(BatchSettings, [LOADER])


##


@settings
class SSHSettings:
    ssh: str | None = option(default=None, help="SSH user & hostname")
    retry: tuple[int, int] | None = option(default=None, help="Retry SSH")
    logger: str | None = option(default=None, help="SSH logger")


SSH_SETTINGS = load_settings(SSHSettings, [LOADER])


##


@settings
class SudoSettings:
    sudo: bool = option(default=False, help="Run as 'sudo'")


SUDO_SETTINGS = load_settings(SudoSettings, [LOADER])


__all__ = [
    "BATCH_SETTINGS",
    "LOADER",
    "SSH_SETTINGS",
    "SUDO_SETTINGS",
    "BatchSettings",
    "SSHSettings",
    "SudoSettings",
]
