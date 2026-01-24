from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import utilities.subprocess
from utilities.constants import HOME
from utilities.core import (
    ReadTextError,
    extract_groups,
    log_info,
    read_text,
    write_text,
)
from utilities.pydantic import extract_secret
from utilities.subprocess import uv_tool_run_cmd

from installer.apps.constants import GITHUB_TOKEN, PATH_BINARIES

if TYPE_CHECKING:
    from utilities.pydantic import SecretLike
    from utilities.types import LoggerLike, PathLike, Retry


def ensure_line(
    path: PathLike, text: str, /, *, logger: LoggerLike | None = None
) -> None:
    try:
        contents = read_text(path)
    except ReadTextError:
        write_text(path, text)
        log_info(logger, "Wrote %r to %r", text, str(path))
        return
    if text not in contents:
        with Path(path).open(mode="a") as fh:
            _ = fh.write(f"\n\n{text}")
        log_info(logger, "Appended %r to %r", text, str(path))


##


def get_home(
    *,
    ssh: str | None = None,
    batch_mode: bool = False,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
) -> Path:
    if ssh is None:
        return HOME
    user, hostname = split_ssh(ssh)
    result = utilities.subprocess.ssh(
        user,
        hostname,
        "getent",
        "passwd",
        user,
        batch_mode=batch_mode,
        return_=True,
        retry=retry,
        logger=logger,
    )
    _, _, _, _, _, home, _ = result.split(":")
    return Path(home)


##


def split_ssh(text: str, /) -> tuple[str, str]:
    user, hostname = extract_groups(r"(.+)@(.+)$", text)
    return user, hostname


##


def ssh_install(
    ssh: str,
    cmd: str,
    /,
    *args: str,
    etc: bool = False,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    token: SecretLike | None = GITHUB_TOKEN,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
) -> None:
    user, hostname = split_ssh(ssh)
    parts: list[str] = []
    if etc:
        parts.append("--etc")
    parts.extend(["--path-binaries", str(path_binaries)])
    if sudo:
        parts.append("--sudo")
    if token is not None:
        parts.extend(["--token", extract_secret(token)])
    utilities.subprocess.ssh(
        user,
        hostname,
        *uv_tool_run_cmd(
            "cli", cmd, *parts, *args, from_="dycw-installer", latest=True
        ),
        retry=retry,
        logger=logger,
    )


__all__ = ["ensure_line", "get_home", "split_ssh", "ssh_install"]
