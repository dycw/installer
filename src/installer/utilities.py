from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, assert_never

import utilities.subprocess
from typed_settings import Secret
from utilities.atomicwrites import writer
from utilities.re import extract_groups
from utilities.text import strip_and_dedent

from installer.apps.constants import SHELL
from installer.logging import LOGGER
from installer.settings import SSH_SETTINGS

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


def ensure_line(text: str, path: PathLike, /) -> None:
    path = Path(path)
    try:
        contents = path.read_text()
    except FileNotFoundError:
        with writer(path) as temp:
            _ = temp.write_text(text)
        LOGGER.info("Wrote %r to %r", text, str(path))
        return
    if text not in contents:
        with path.open(mode="a") as fh:
            _ = fh.write(f"\n\n{text}")
        LOGGER.info("Appended %r to %r", text, str(path))


##


def ensure_shell_rc(text: str, /, *, etc: str | None = None) -> None:
    if etc is None:
        match SHELL:
            case "bash" | "zsh":
                path = Path.home() / f".{SHELL}rc"
            case "fish":
                path = Path.home() / ".config/fish/config.fish"
            case "posix":
                msg = f"Invalid shell: {SHELL=}"
                raise TypeError(msg)
            case never:
                assert_never(never)
        ensure_line(text, path)
    else:
        match SHELL:
            case "bash" | "zsh":
                full = strip_and_dedent(f"""
                    #!/usr/bin/env sh
                    {text}
                """)
                path = Path(f"/etc/profile.d/{etc}.sh")
                ensure_line(full, path)
            case "fish" | "posix":
                msg = f"Invalid shell: {SHELL!r}"
                raise TypeError(msg)
            case never:
                assert_never(never)


##


def get_home(
    *,
    ssh: str | None = SSH_SETTINGS.ssh,
    retry: Retry | None = SSH_SETTINGS.retry,
    logger: LoggerLike | None = SSH_SETTINGS.logger,
) -> Path:
    if ssh is None:
        return Path.home()
    user, hostname = split_ssh(ssh)
    result = utilities.subprocess.ssh(
        user,
        hostname,
        "getent",
        "passwd",
        user,
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


__all__ = ["convert_token", "ensure_line", "ensure_shell_rc", "split_ssh"]
