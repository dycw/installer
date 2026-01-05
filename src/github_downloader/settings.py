from __future__ import annotations

from pathlib import Path

from typed_settings import EnvLoader, Secret, load_settings, option, secret, settings

from github_downloader.constants import MACHINE_TYPE, SYSTEM_NAME

LOADER = EnvLoader("")


@settings
class Settings:
    owner: str = option(help="Repository owner")
    repo: str = option(help="Repository name")
    binary_name: str = option(help="Binary name")
    token: Secret[str] | None = secret(default=None, help="The GitHub token")
    match_system: bool = option(default=False, help="Match the system name")
    system_name: str = option(default=SYSTEM_NAME, help="System name")
    match_machine: bool = option(default=False, help="Match the machine type")
    machine_type: str = option(default=MACHINE_TYPE, help="Machine type")
    not_endswith: list[str] = option(factory=list, help="Asset name endings to exclude")
    timeout: int = option(default=60, help="Download timeout")
    path_binaries: Path = option(
        default=Path("/usr/local/bin"), help="Path to all binaries"
    )
    chunk_size: int = option(default=8192, help="Streaming chunk size")
    permissions: str = option(default="u=rwx,g=rx,o=rx", help="Binary permissions")


SETTINGS = load_settings(Settings, [LOADER])


__all__ = ["LOADER", "SETTINGS", "Settings"]
