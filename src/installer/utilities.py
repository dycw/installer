from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import utilities.subprocess
from utilities.core import (
    Permissions,
    PermissionsLike,
    ReadTextError,
    always_iterable,
    extract_groups,
    normalize_str,
    read_text,
    write_text,
)
from utilities.pydantic import extract_secret
from utilities.subprocess import uv_tool_run_cmd

if TYPE_CHECKING:
    from utilities.pydantic import SecretLike
    from utilities.shellingham import Shell
    from utilities.types import LoggerLike, MaybeSequenceStr, PathLike, Retry


def ensure_line_or_lines(
    path: PathLike,
    line_or_lines: MaybeSequenceStr,
    /,
    *,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
) -> None:
    text = normalize_str("\n".join(always_iterable(line_or_lines)))
    try:
        contents = read_text(path)
    except ReadTextError:
        write_text(path, text, perms=perms, owner=owner, group=group)
        return
    if text not in contents:
        with Path(path).open(mode="a") as fh:
            _ = fh.write(f"\n\n{text}")


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
    group: str | int | None = None,
    home: PathLike | None = None,
    owner: str | int | None = None,
    path_binaries: PathLike | None = None,
    perms: PermissionsLike | None = None,
    perms_binary: PermissionsLike | None = None,
    perms_config: PermissionsLike | None = None,
    root: PathLike | None = None,
    shell: Shell | None = None,
    starship_toml: PathLike | None = None,
    sudo: bool = False,
    token: SecretLike | None = None,
    user: str | None = None,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
) -> None:
    ssh_user, ssh_hostname = split_ssh(ssh)
    parts: list[str] = []
    if etc:
        parts.append("--etc")
    if group is not None:
        parts.extend(["--group", str(group)])
    if home is not None:
        parts.extend(["--home", str(home)])
    if owner is not None:
        parts.extend(["--owner", str(owner)])
    if path_binaries is not None:
        parts.extend(["--path-binaries", str(path_binaries)])
    if perms is not None:
        parts.extend(["--perms", str(Permissions.new(perms))])
    if perms_binary is not None:
        parts.extend(["--perms-binary", str(Permissions.new(perms_binary))])
    if perms_config is not None:
        parts.extend(["--perms-config", str(Permissions.new(perms_config))])
    if root is not None:
        parts.extend(["--root", str(root)])
    if shell is not None:
        parts.extend(["--shell", shell])
    if starship_toml is not None:
        parts.extend(["--starship-toml", str(starship_toml)])
    if sudo:
        parts.append("--sudo")
    if token is not None:
        parts.extend(["--token", extract_secret(token)])
    if user is not None:
        parts.extend(["--user", user])
    utilities.subprocess.ssh(
        ssh_user,
        ssh_hostname,
        *uv_tool_run_cmd(
            "cli", cmd, *parts, *args, from_="dycw-installer", latest=True
        ),
        retry=retry,
        logger=logger,
    )


__all__ = ["ensure_line_or_lines", "split_ssh", "ssh_install"]
