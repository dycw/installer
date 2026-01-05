from __future__ import annotations

from pathlib import Path

from typed_settings import EnvLoader, Secret, load_settings, option, secret, settings

from github_downloader.constants import MACHINE_TYPE, SYSTEM_NAME
from github_downloader.utilities import convert_token

LOADER = EnvLoader("")


@settings
class CommonSettings:
    token: Secret[str] | None = secret(
        default=None, converter=convert_token, help="The GitHub token"
    )
    match_system: bool = option(
        default=False, help=f"Match the system name {SYSTEM_NAME!r}"
    )
    match_machine: bool = option(
        default=False, help=f"Match the machine type {MACHINE_TYPE!r}"
    )
    not_endswith: list[str] = option(factory=list, help="Asset name endings to exclude")
    timeout: int = option(default=60, help="Download timeout")
    chunk_size: int = option(default=8196, help="Streaming chunk size")


COMMON_SETTINGS = load_settings(CommonSettings, [LOADER])


@settings
class PermSettings:
    sudo: bool = option(default=False, help="Call 'mv' with 'sudo'")
    perms: str | None = option(default=None, help="Change permissions")
    owner: str | None = option(default=None, help="Change owner")
    group: str | None = option(default=None, help="Change group")


PERM_SETTINGS = load_settings(PermSettings, [LOADER])


@settings
class AgeSettings:
    binary_name: str = option(default="age", help="Binary name")


AGE_SETTINGS = load_settings(AgeSettings, [LOADER])


@settings
class PathBinariesSettings:
    path_binaries: Path = option(
        default=Path("/usr/local/bin/"), help="Path to the binaries"
    )


PATH_BINARIES_SETTINGS = load_settings(PathBinariesSettings, [LOADER])


@settings
class SopsSettings:
    binary_name: str = option(default="sops", help="Binary name")


SOPS_SETTINGS = load_settings(SopsSettings, [LOADER])


__all__ = [
    "AGE_SETTINGS",
    "COMMON_SETTINGS",
    "LOADER",
    "PATH_BINARIES_SETTINGS",
    "PERM_SETTINGS",
    "SOPS_SETTINGS",
    "AgeSettings",
    "CommonSettings",
    "PathBinariesSettings",
    "PermSettings",
    "SopsSettings",
]
