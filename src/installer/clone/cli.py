from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import click
from click import argument
from typed_settings import click_options
from utilities.logging import basic_config
from utilities.os import is_pytest

from installer.clone.lib import git_clone_with
from installer.clone.settings import CloneSettings
from installer.logging import LOGGER
from installer.settings import LOADER

if TYPE_CHECKING:
    from utilities.types import PathLike


@argument("path_key", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@argument("host", type=str)
@argument("owner", type=str)
@argument("repo", type=str)
@click_options(CloneSettings, [LOADER], show_envvars_in_help=True, argname="clone")
def git_clone_with_sub_cmd(
    *, path_key: PathLike, host: str, owner: str, repo: str, clone: CloneSettings
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    git_clone_with(
        path_key,
        host,
        owner,
        repo,
        port=clone.port,
        path_clone=clone.path_clone,
        branch=clone.branch,
    )


__all__ = ["git_clone_with_sub_cmd"]
