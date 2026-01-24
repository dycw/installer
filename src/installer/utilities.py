from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, assert_never

import utilities.subprocess
from typed_settings import Secret
from utilities.constants import HOME
from utilities.core import (
    ReadTextError,
    extract_groups,
    log_info,
    read_text,
    write_text,
)
from utilities.subprocess import uv_tool_run_cmd

from installer.logging import LOGGER

if TYPE_CHECKING:
    from utilities.types import LoggerLike, PathLike, Retry


def convert_token(x: str | None, /) -> Secret[str] | None:
    match x:
        case Secret():
            match x.get_secret_value():
                case None:
                    return None
                case str() as inner:
                    y = inner.strip("\n")
                    return None if y == "" else Secret(y)
                case never:
                    assert_never(never)
        case str():
            y = x.strip("\n")
            return None if y == "" else Secret(y)
        case None:
            return None
        case never:
            assert_never(never)


##


def ensure_line(path: PathLike, text: str, /, *, logger: LoggerLike = LOGGER) -> None:
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
    logger: LoggerLike = LOGGER,
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
    sudo: bool = False,
    etc: bool = False,
    retry: Retry | None = None,
    logger: LoggerLike = LOGGER,
) -> None:
    user, hostname = split_ssh(ssh)
    parts: list[str] = []
    if sudo:
        parts.append("--sudo")
    if etc:
        parts.append("--etc")
    utilities.subprocess.ssh(
        user,
        hostname,
        *uv_tool_run_cmd(
            "cli", cmd, *parts, *args, from_="dycw-installer", latest=True
        ),
        retry=retry,
        logger=logger,
    )


__all__ = ["convert_token", "ensure_line", "get_home", "split_ssh", "ssh_install"]
