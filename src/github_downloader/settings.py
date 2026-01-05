from __future__ import annotations

from pathlib import Path
from platform import machine, system

from typed_settings import EnvLoader, Secret, load_settings, option, secret, settings

LOADER = EnvLoader("")


@settings
class Settings:
    owner: str = option(help="Repository owner")
    repo: str = option(help="Repository name")
    token: Secret[str] | None = secret(default=None, help="The GitHub token")
    system: str = option(default=system(), help="System name")
    machine: str = option(default=machine(), help="Machine type")
    binaries: Path = option(default=Path("/usr/local/bin"), help="Path to all binaries")
    timeout: int = option(default=60, help="Download timeout")
    chunk_size: int = option(default=8192, help="Streaming chunk size")


SETTINGS = load_settings(Settings, [LOADER])


__all__ = ["LOADER", "SETTINGS", "Settings"]
