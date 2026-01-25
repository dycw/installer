from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import utilities.subprocess
from utilities.core import (
    Permissions,
    PermissionsLike,
    ReadTextError,
    extract_groups,
    log_info,
    read_text,
    write_text,
)
from utilities.pydantic import extract_secret
from utilities.subprocess import uv_tool_run_cmd

from installer.apps.constants import GITHUB_TOKEN, PATH_BINARIES, PERMISSIONS

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


def split_ssh(text: str, /) -> tuple[str, str]:
    user, hostname = extract_groups(r"(.+)@(.+)$", text)
    return user, hostname


##


def ssh_install(
    ssh: str,
    cmd: str,
    /,
    *args: str,
    custom_shell_config: bool = False,
    etc: bool = False,
    group: str | int | None = None,
    owner: str | int | None = None,
    path_binaries: PathLike = PATH_BINARIES,
    perms: PermissionsLike = PERMISSIONS,
    sudo: bool = False,
    token: SecretLike | None = GITHUB_TOKEN,
    user: str | None = None,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
) -> None:
    user, hostname = split_ssh(ssh)
    parts: list[str] = []
    if custom_shell_config:
        parts.append("--custom-shell-config")
    if etc:
        parts.append("--etc")
    if group is not None:
        parts.extend(["--group", str(group)])
    if owner is not None:
        parts.extend(["--owner", str(owner)])
    parts.extend([
        "--path-binaries",
        str(path_binaries),
        "--perms",
        str(Permissions.new(perms)),
    ])
    if sudo:
        parts.append("--sudo")
    if token is not None:
        parts.extend(["--token", extract_secret(token)])
    if user is not None:
        parts.extend(["--user", user])
    utilities.subprocess.ssh(
        user,
        hostname,
        *uv_tool_run_cmd(
            "cli", cmd, *parts, *args, from_="dycw-installer", latest=True
        ),
        retry=retry,
        logger=logger,
    )


__all__ = ["ensure_line", "split_ssh", "ssh_install"]
