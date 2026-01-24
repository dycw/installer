from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import utilities.subprocess
from utilities.core import write_text
from utilities.subprocess import cp
from utilities.tabulate import func_param_desc

from installer import __version__
from installer.clone.settings import CLONE_SETTINGS
from installer.configs.lib import setup_ssh_config
from installer.configs.settings import FILE_SYSTEM_ROOT
from installer.constants import RELATIVE_HOME

if TYPE_CHECKING:
    from collections.abc import Iterator

    from utilities.types import PathLike


def git_clone(
    key: PathLike,
    owner: str,
    repo: str,
    /,
    *,
    host: str = CLONE_SETTINGS.host,
    port: int | None = CLONE_SETTINGS.port,
    dest: PathLike = CLONE_SETTINGS.dest,
    branch: str | None = CLONE_SETTINGS.branch,
    __root: PathLike = FILE_SYSTEM_ROOT,
) -> None:
    log_info(
        logger,
        func_param_desc(
            git_clone,
            __version__,
            f"{key=}",
            f"{owner=}",
            f"{repo=}",
            f"{host=}",
            f"{port=}",
            f"{dest=}",
            f"{branch=}",
        ),
    )
    key = Path(key)
    setup_ssh_config()
    _setup_deploy_key(key, host=host, port=port, __root=__root)
    utilities.subprocess.git_clone(
        f"git@{key.stem}:{owner}/{repo}", dest, branch=branch
    )


def _setup_deploy_key(
    path: PathLike,
    /,
    *,
    host: str = CLONE_SETTINGS.host,
    port: int | None = CLONE_SETTINGS.port,
    __root: PathLike = FILE_SYSTEM_ROOT,
) -> None:
    path = Path(path)
    stem = path.stem
    path_config = _get_path_config(stem, __root=__root)
    text = "\n".join(_yield_config_lines(stem, host=host, port=port))
    write_text(path_config, text, overwrite=True)
    dest = _get_path_deploy_key(stem, __root=__root)
    cp(path, dest, perms="u=rw,g=,o=")


def _get_path_config(stem: str, /, *, __root: PathLike = FILE_SYSTEM_ROOT) -> Path:
    home = Path(__root, RELATIVE_HOME)
    return home / f".ssh/config.d/{stem}.conf"


def _yield_config_lines(
    stem: str,
    /,
    *,
    host: str = CLONE_SETTINGS.host,
    port: int | None = CLONE_SETTINGS.port,
    __root: PathLike = FILE_SYSTEM_ROOT,
) -> Iterator[str]:
    path_key = _get_path_deploy_key(stem, __root=__root)
    yield f"Host {stem}"
    indent = 4 * " "
    yield f"{indent}User git"
    yield f"{indent}HostName {host}"
    if port is not None:
        yield (f"{indent}Port {port}")
    yield f"{indent}IdentityFile {path_key}"
    yield f"{indent}IdentitiesOnly yes"


def _get_path_deploy_key(stem: str, /, *, __root: PathLike = FILE_SYSTEM_ROOT) -> Path:
    home = Path(__root, RELATIVE_HOME)
    return home / ".ssh/deploy-keys" / stem


__all__ = ["git_clone"]
