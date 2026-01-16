from __future__ import annotations

from pathlib import Path

from typed_settings import load_settings, option, settings

from installer.settings import LOADER


@settings
class CloneSettings:
    port: int | None = option(default=None, help="Clone port")
    path_clone: Path = option(default=Path.cwd(), help="Path to clone to")
    branch: str | None = option(default=None, help="Branch to check out")


CLONE_SETTINGS = load_settings(CloneSettings, [LOADER])


__all__ = ["CLONE_SETTINGS", "CloneSettings"]
