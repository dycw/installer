from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from utilities.atomicwrites import writer
from utilities.subprocess import cp, git_clone
from utilities.tabulate import func_param_desc

from installer import __version__
from installer.clone.settings import CLONE_SETTINGS
from installer.configs.lib import setup_ssh_config
from installer.logging import LOGGER

if TYPE_CHECKING:
    from collections.abc import Iterator

    from utilities.types import PathLike


def git_clone_with(
    path_key: PathLike,
    host: str,
    owner: str,
    repo: str,
    /,
    *,
    port: int | None = CLONE_SETTINGS.port,
    path_clone: PathLike = CLONE_SETTINGS.path_clone,
    branch: str | None = CLONE_SETTINGS.branch,
) -> None:
    LOGGER.info(
        func_param_desc(
            git_clone_with,
            __version__,
            f"{path_key=}",
            f"{host=}",
            f"{owner=}",
            f"{repo=}",
            f"{port=}",
            f"{path_clone=}",
            f"{branch=}",
        )
    )
    path_key = Path(path_key)
    setup_ssh_config()
    _setup_deploy_key(path_key, host, port=port)
    git_clone(f"git@{path_key.stem}:{owner}/{repo}", path_clone, branch=branch)


def _setup_deploy_key(
    path: PathLike, host: str, /, *, port: int | None = CLONE_SETTINGS.port
) -> None:
    path = Path(path)
    stem = path.stem
    path_config = _get_path_config(stem)
    text = "\n".join(_yield_config_lines(stem, host, port=port)) + "\n"
    with writer(path_config, overwrite=True) as temp:
        _ = temp.write_text(text)
    dest = _get_path_deploy_key(stem)
    cp(path, dest, perms="u=rw,g=,o=")


def _get_path_config(stem: str, /) -> Path:
    return Path.home() / f".ssh/config.d/{stem}.conf"


def _yield_config_lines(
    stem: str, host: str, /, *, port: int | None = CLONE_SETTINGS.port
) -> Iterator[str]:
    path_key = _get_path_deploy_key(stem)
    yield f"Host {stem}"
    indent = 4 * " "
    yield f"{indent}User git"
    yield f"{indent}HostName {host}"
    if port is not None:
        yield (f"{indent}Port {port}")
    yield f"{indent}IdentityFile {path_key}"
    yield f"{indent}IdentitiesOnly yes"


def _get_path_deploy_key(stem: str, /) -> Path:
    return Path.home() / ".ssh/deploy-keys" / stem


__all__ = ["git_clone_with"]
