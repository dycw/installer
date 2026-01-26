from __future__ import annotations

from click import option
from utilities.click import Path, Str

from installer.apps.constants import GITHUB_TOKEN, PATH_BINARIES, PERMISSIONS

group_option = option("--group", type=Str(), default=None, help="Binary group")
owner_option = option("--owner", type=Str(), default=None, help="Binary owner")
path_binaries_option = option(
    "--path-binaries",
    type=Path(exist="dir if exists"),
    default=PATH_BINARIES,
    help="Path to the binaries",
)
perms_option = option(
    "--perms", type=Str(), default=PERMISSIONS, help="Binary permissions"
)
token_option = option("--token", type=Str(), default=GITHUB_TOKEN, help="GitHub token")


__all__ = [
    "group_option",
    "owner_option",
    "path_binaries_option",
    "perms_option",
    "token_option",
]
