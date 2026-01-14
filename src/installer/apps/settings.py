from __future__ import annotations

from os import environ
from pathlib import Path

from typed_settings import Secret, load_settings, option, secret, settings

from installer.utilities import LOADER, convert_token


@settings
class DownloadSettings:
    token: Secret[str] | None = secret(
        default=None if (t := environ.get("GITHUB_TOKEN")) is None else Secret(t),
        converter=convert_token,
        help="The GitHub token",
    )
    timeout: int = option(default=60, help="Download timeout")
    chunk_size: int = option(default=8196, help="Streaming chunk size")


DOWNLOAD_SETTINGS = load_settings(DownloadSettings, [LOADER])


##


@settings
class MatchSettings:
    match_system: bool = option(default=False, help="Match the system name")
    match_c_std_lib: bool = option(default=False, help="Match the C standard library")
    match_machine: bool = option(default=False, help="Match the machine type")
    not_matches: list[str] = option(
        factory=list, help="Asset name patterns to not match again"
    )
    not_endswith: list[str] = option(factory=list, help="Asset name endings to exclude")


MATCH_SETTINGS = load_settings(MatchSettings, [LOADER])


##


@settings
class PathBinariesSettings:
    path_binaries: Path = option(
        default=Path("/usr/local/bin/"), help="Path to the binaries"
    )


PATH_BINARIES_SETTINGS = load_settings(PathBinariesSettings, [LOADER])


##


@settings
class PermsSettings:
    perms: str = option(default="u=rwx,g=rx,o=rx", help="Change permissions")
    owner: str | None = option(default=None, help="Change owner")
    group: str | None = option(default=None, help="Change group")


PERMS_SETTINGS = load_settings(PermsSettings, [LOADER])


##


@settings
class ShellRcSettings:
    skip_shell_rc: bool = option(
        default=False, help="Skip setting up the shell configs"
    )
    etc: bool = option(default=False, help="Set up shell configs in '/etc'")


SHELL_RC_SETTINGS = load_settings(ShellRcSettings, [LOADER])


##


@settings
class TagSettings:
    tag: str | None = secret(default=None, help="The GitHub release tag")


TAG_SETTINGS = load_settings(TagSettings, [LOADER])


__all__ = [
    "DOWNLOAD_SETTINGS",
    "MATCH_SETTINGS",
    "PATH_BINARIES_SETTINGS",
    "PERMS_SETTINGS",
    "SHELL_RC_SETTINGS",
    "TAG_SETTINGS",
    "DownloadSettings",
    "MatchSettings",
    "PathBinariesSettings",
    "PermsSettings",
    "ShellRcSettings",
    "TagSettings",
]
