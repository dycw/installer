from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import click
from click import argument
from typed_settings import click_options
from utilities.core import is_pytest
from utilities.logging import basic_config

from installer.clone.lib import git_clone
from installer.clone.settings import CloneSettings
from installer.configs.settings import RootSettings
from installer.logging import LOGGER
from installer.settings import LOADER

if TYPE_CHECKING:
    from utilities.types import PathLike


@argument("key", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@argument("owner", type=str)
@argument("repo", type=str)
@click_options(CloneSettings, [LOADER], show_envvars_in_help=True, argname="clone")
@click_options(RootSettings, [LOADER], show_envvars_in_help=True, argname="root")
def git_clone_sub_cmd(
    *, key: PathLike, owner: str, repo: str, clone: CloneSettings, root: RootSettings
) -> None:
    """Clone a repo with a deploy key."""
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    git_clone(
        key,
        owner,
        repo,
        root=root.root,
        host=clone.host,
        port=clone.port,
        dest=clone.dest,
        branch=clone.branch,
    )


__all__ = ["git_clone_sub_cmd"]
