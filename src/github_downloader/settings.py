from __future__ import annotations

from typing import TYPE_CHECKING, Any

from attrs import fields_dict
from typed_settings import EnvLoader, Secret, load_settings, option, secret, settings

from github_downloader.constants import MACHINE_TYPE, SYSTEM_NAME
from github_downloader.utilities import convert_token

if TYPE_CHECKING:
    from pathlib import Path

LOADER = EnvLoader("")


def _get_help(cls: type[Any], member_descriptor: Any, /) -> None:
    return fields_dict(cls)[member_descriptor.__name__].metadata["typed-settings"][
        "help"
    ]


@settings
class YieldAssetSettings:
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


YIELD_ASSET_SETTINGS = load_settings(YieldAssetSettings, [LOADER])


@settings
class SetupAssetSettings:
    token: Secret[str] | None = secret(
        default=YIELD_ASSET_SETTINGS.token,
        converter=convert_token,
        help=_get_help(YieldAssetSettings, YieldAssetSettings.token),
    )
    match_system: bool = option(
        default=YIELD_ASSET_SETTINGS.match_system,
        help=_get_help(YieldAssetSettings, YieldAssetSettings.match_system),
    )
    match_machine: bool = option(
        default=YIELD_ASSET_SETTINGS.match_machine,
        help=_get_help(YieldAssetSettings, YieldAssetSettings.match_machine),
    )
    not_endswith: list[str] = option(
        default=YIELD_ASSET_SETTINGS.not_endswith,
        help=_get_help(YieldAssetSettings, YieldAssetSettings.not_endswith),
    )
    timeout: int = option(
        default=YIELD_ASSET_SETTINGS.timeout,
        help=_get_help(YieldAssetSettings, YieldAssetSettings.timeout),
    )
    chunk_size: int = option(
        default=YIELD_ASSET_SETTINGS.chunk_size,
        help=_get_help(YieldAssetSettings, YieldAssetSettings.chunk_size),
    )
    sudo: bool = option(default=False, help="Call 'mv' with 'sudo'")
    perms: str | None = option(default=None, help="Change permissions")
    owner: str | None = option(default=None, help="Change owner")
    group: str | None = option(default=None, help="Change group")


SETTINGS = load_settings(SetupAssetSettings, [LOADER])


@settings
class AgeSettings:
    binary_name: str = option(default="age", help="Binary name")
    token: Secret[str] | None = secret(
        default=YIELD_ASSET_SETTINGS.token,
        converter=convert_token,
        help=_get_help(YieldAssetSettings, YieldAssetSettings.token),
    )
    timeout: int = option(
        default=YIELD_ASSET_SETTINGS.timeout,
        help=_get_help(YieldAssetSettings, YieldAssetSettings.timeout),
    )
    chunk_size: int = option(
        default=YIELD_ASSET_SETTINGS.chunk_size,
        help=_get_help(YieldAssetSettings, YieldAssetSettings.chunk_size),
    )
    timeout: int = option(
        default=SETTINGS.timeout, help=_get_help(SetupAssetSettings.timeout)
    )
    path_binaries: Path = option(
        default=SETTINGS.path_binaries, help=_get_help(SetupAssetSettings.path_binaries)
    )
    permissions: str = option(
        default=SETTINGS.perms, help=_get_help(SetupAssetSettings.perms)
    )


AGE_SETTINGS = load_settings(AgeSettings, [LOADER])


@settings
class SopsSettings:
    binary_name: str = option(default="sops", help="Binary name")
    token: Secret[str] | None = secret(
        default=SETTINGS.token,
        converter=convert_token,
        help=_get_help(SetupAssetSettings.token),
    )
    timeout: int = option(
        default=SETTINGS.timeout, help=_get_help(SetupAssetSettings.timeout)
    )
    path_binaries: Path = option(
        default=SETTINGS.path_binaries, help=_get_help(SetupAssetSettings.path_binaries)
    )
    chunk_size: int = option(
        default=SETTINGS.chunk_size, help=_get_help(SetupAssetSettings.chunk_size)
    )
    permissions: str = option(
        default=SETTINGS.perms, help=_get_help(SetupAssetSettings.perms)
    )


SOPS_SETTINGS = load_settings(SopsSettings, [LOADER])


__all__ = [
    "AGE_SETTINGS",
    "LOADER",
    "SETTINGS",
    "SOPS_SETTINGS",
    "YIELD_ASSET_SETTINGS",
    "AgeSettings",
    "SetupAssetSettings",
    "SopsSettings",
    "YieldAssetSettings",
]
