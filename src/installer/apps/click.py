from __future__ import annotations

from pathlib import Path

import click
from click import option

from installer.apps.constants import GITHUB_TOKEN, PATH_BINARIES

group_option = option(
    "--group", type=click.Path(path_type=Path), default=None, help="Binary group"
)
owner_option = option(
    "--owner", type=click.Path(path_type=Path), default=None, help="Binary owner"
)
path_binaries_option = option(
    "--path-binaries",
    type=click.Path(path_type=Path),
    default=PATH_BINARIES,
    help="Path to the binaries",
)
perms_option = option("--perms", type=str, default=None, help="Binary permissions")
token_option = option("--token", type=str, default=GITHUB_TOKEN, help="GitHub token")


__all__ = [
    "group_option",
    "owner_option",
    "path_binaries_option",
    "perms_option",
    "token_option",
]
