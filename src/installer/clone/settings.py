from __future__ import annotations

from pathlib import Path

from typed_settings import load_settings, option, settings

from installer.settings import LOADER

GIT_CLONE_HOST = "github.com"


@settings
class CloneSettings:
    host: str = option(default="github.com", help="Repository host")
    port: int | None = option(default=None, help="Repository port")
    dest: Path = option(default=Path.cwd(), help="Path to clone to")
    branch: str | None = option(default=None, help="Branch to check out")


CLONE_SETTINGS = load_settings(CloneSettings, [LOADER])


__all__ = ["CLONE_SETTINGS", "CloneSettings"]
