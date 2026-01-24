from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import click
from click import argument, option
from utilities.core import is_pytest
from utilities.logging import basic_config

from installer.click import logger_option, retry_option, ssh_option
from installer.clone.lib import git_clone
from installer.clone.settings import GIT_CLONE_HOST

if TYPE_CHECKING:
    from utilities.types import LoggerLike, PathLike, Retry


@argument("key", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@argument("owner", type=str)
@argument("repo", type=str)
@logger_option
@ssh_option
@retry_option
@option("--host", type=str, default=GIT_CLONE_HOST, help="Repository host")
@option("--port", type=int, default=None, help="Repository port")
@option(
    "--dest",
    type=click.Path(file_okay=False, path_type=Path),
    default=None,
    help="Path to clone to",
)
@option("--branch", type=str, default=None, help="Branch to check out")
def git_clone_sub_cmd(
    *,
    key: PathLike,
    owner: str,
    repo: str,
    logger: LoggerLike | None,
    ssh: str | None,
    retry: Retry | None,
    host: str,
    port: int | None,
    dest: PathLike,
    branch: str | None,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    git_clone(
        key,
        owner,
        repo,
        logger=logger,
        ssh=ssh,
        retry=retry,
        host=host,
        port=port,
        dest=dest,
        branch=branch,
    )


__all__ = ["git_clone_sub_cmd"]
