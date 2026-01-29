from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import utilities.subprocess
from utilities.constants import HOME, PWD
from utilities.core import always_iterable, log_info, write_text
from utilities.subprocess import _HOST_KEY_ALGORITHMS, cp, ssh_keyscan

from installer.clone.constants import GIT_CLONE_HOST
from installer.configs.lib import setup_ssh_config

if TYPE_CHECKING:
    from collections.abc import Iterator

    from utilities.types import LoggerLike, PathLike, Retry


def git_clone(
    key: PathLike,
    owner: str,
    repo: str,
    /,
    *,
    logger: LoggerLike | None = None,
    home: PathLike = HOME,
    host: str = GIT_CLONE_HOST,
    retry: Retry | None = None,
    port: int | None = None,
    dest: PathLike = PWD,
    branch: str | None = None,
) -> None:
    log_info(logger, "Cloning repository...")
    _git_clone_prepare(key, logger=logger, home=home, host=host, retry=retry, port=port)
    stem = Path(key).stem
    utilities.subprocess.git_clone(f"git@{stem}:{owner}/{repo}", dest, branch=branch)


def _git_clone_prepare(
    key: PathLike,
    /,
    *,
    logger: LoggerLike | None = None,
    home: PathLike = HOME,
    host: str = GIT_CLONE_HOST,
    retry: Retry | None = None,
    port: int | None = None,
) -> None:
    key = Path(key)
    setup_ssh_config(logger=logger, home=home)
    _setup_deploy_key(key, home=home, host=host, port=port)
    _setup_known_hosts(host=host, home=home, retry=retry, port=port)


def _setup_deploy_key(
    path: PathLike,
    /,
    *,
    home: PathLike = HOME,
    host: str = GIT_CLONE_HOST,
    port: int | None = None,
) -> None:
    path = Path(path)
    stem = path.stem
    path_config = _get_path_config(stem, home=home)
    text = "\n".join(_yield_config_lines(stem, home=home, host=host, port=port))
    write_text(path_config, text, overwrite=True)
    dest = _get_path_deploy_key(stem, home=home)
    cp(path, dest, perms="u=rw,g=,o=")


def _get_path_config(stem: str, /, *, home: PathLike = HOME) -> Path:
    return Path(home, f".ssh/config.d/{stem}.conf")


def _yield_config_lines(
    stem: str,
    /,
    *,
    home: PathLike = HOME,
    host: str = GIT_CLONE_HOST,
    port: int | None = None,
) -> Iterator[str]:
    yield f"Host {stem}"
    for line in _yield_config_lines_core(stem, home=home, host=host, port=port):
        yield f"    {line}"


def _yield_config_lines_core(
    stem: str,
    /,
    *,
    home: PathLike = HOME,
    host: str = GIT_CLONE_HOST,
    port: int | None = None,
) -> Iterator[str]:
    yield "User git"
    yield f"HostName {host}"
    if port is not None:
        yield f"Port {port}"
    yield f"IdentityFile {_get_path_deploy_key(stem, home=home)}"
    yield "IdentitiesOnly yes"
    yield "BatchMode yes"
    yield f"HostKeyAlgorithms {','.join(always_iterable(_HOST_KEY_ALGORITHMS))}"
    yield "StrictHostKeyChecking yes"


def _get_path_deploy_key(stem: str, /, *, home: PathLike = HOME) -> Path:
    return Path(home, ".ssh/deploy-keys", stem)


def _setup_known_hosts(
    *,
    host: str = GIT_CLONE_HOST,
    home: PathLike = HOME,
    retry: Retry | None = None,
    port: int | None = None,
) -> None:
    ssh_keyscan(host, path=Path(home, ".ssh/known_hosts"), retry=retry, port=port)


__all__ = ["git_clone"]
