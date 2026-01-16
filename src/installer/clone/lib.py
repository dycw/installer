from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import utilities.subprocess
from utilities.atomicwrites import writer
from utilities.subprocess import cp
from utilities.tabulate import func_param_desc

from installer import __version__
from installer.clone.settings import CLONE_SETTINGS
from installer.configs.lib import setup_ssh_config
from installer.configs.settings import ROOT_SETTINGS
from installer.constants import RELATIVE_HOME
from installer.logging import LOGGER

if TYPE_CHECKING:
    from collections.abc import Iterator

    from utilities.types import PathLike


def git_clone(
    key: PathLike,
    owner: str,
    repo: str,
    /,
    *,
    root: PathLike = ROOT_SETTINGS.root,
    host: str = CLONE_SETTINGS.host,
    port: int | None = CLONE_SETTINGS.port,
    dest: PathLike = CLONE_SETTINGS.dest,
    branch: str | None = CLONE_SETTINGS.branch,
) -> None:
    LOGGER.info(
        func_param_desc(
            git_clone,
            __version__,
            f"{key=}",
            f"{owner=}",
            f"{repo=}",
            f"{root=}",
            f"{host=}",
            f"{port=}",
            f"{dest=}",
            f"{branch=}",
        )
    )
    key = Path(key)
    setup_ssh_config()
    _setup_deploy_key(key, root=root, host=host, port=port)
    utilities.subprocess.git_clone(
        f"git@{key.stem}:{owner}/{repo}", dest, branch=branch
    )


def _setup_deploy_key(
    path: PathLike,
    /,
    *,
    root: PathLike = ROOT_SETTINGS.root,
    host: str = CLONE_SETTINGS.host,
    port: int | None = CLONE_SETTINGS.port,
) -> None:
    path = Path(path)
    stem = path.stem
    path_config = _get_path_config(stem, root=root)
    text = "\n".join(_yield_config_lines(stem, host=host, port=port)) + "\n"
    with writer(path_config, overwrite=True) as temp:
        _ = temp.write_text(text)
    dest = _get_path_deploy_key(stem, root=root)
    cp(path, dest, perms="u=rw,g=,o=")


def _get_path_config(stem: str, /, *, root: PathLike = ROOT_SETTINGS.root) -> Path:
    home = Path(root, RELATIVE_HOME)
    return home / f".ssh/config.d/{stem}.conf"


def _yield_config_lines(
    stem: str,
    /,
    *,
    root: PathLike = ROOT_SETTINGS.root,
    host: str = CLONE_SETTINGS.host,
    port: int | None = CLONE_SETTINGS.port,
) -> Iterator[str]:
    path_key = _get_path_deploy_key(stem, root=root)
    yield f"Host {stem}"
    indent = 4 * " "
    yield f"{indent}User git"
    yield f"{indent}HostName {host}"
    if port is not None:
        yield (f"{indent}Port {port}")
    yield f"{indent}IdentityFile {path_key}"
    yield f"{indent}IdentitiesOnly yes"


def _get_path_deploy_key(stem: str, /, *, root: PathLike = ROOT_SETTINGS.root) -> Path:
    home = Path(root, RELATIVE_HOME)
    return home / ".ssh/deploy-keys" / stem


__all__ = ["git_clone"]
