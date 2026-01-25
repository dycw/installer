from __future__ import annotations

from pathlib import Path
from shlex import join
from typing import TYPE_CHECKING, assert_never

import utilities.subprocess
from utilities.constants import HOME
from utilities.core import (
    log_info,
    normalize_multi_line_str,
    normalize_str,
    repr_str,
    write_text,
)
from utilities.shellingham import SHELL
from utilities.subprocess import BASH_LS, maybe_sudo_cmd, mkdir_cmd, tee, tee_cmd

from installer.configs.constants import FILE_SYSTEM_ROOT
from installer.utilities import ensure_line, split_ssh

if TYPE_CHECKING:
    from utilities.types import LoggerLike, PathLike, Retry


def setup_authorized_keys(
    keys: list[str],
    /,
    *,
    logger: LoggerLike | None = None,
    home: PathLike = HOME,
    ssh: str | None = None,
    batch_mode: bool = False,
    retry: Retry | None = None,
) -> None:
    """Set up the SSH authorized keys."""
    log_info(logger, "Setting up authorized keys...")
    path = Path(home, ".ssh/authorized_keys")
    text = normalize_str("\n".join(keys))
    if ssh is None:
        write_text(path, text, overwrite=True)
    else:
        user, hostname = split_ssh(ssh)
        utilities.subprocess.ssh(
            user,
            hostname,
            *tee_cmd(path),
            batch_mode=batch_mode,
            input=text,
            retry=retry,
            logger=logger,
        )


##


def setup_shell_config(
    bash: str,
    fish: str,
    /,
    *,
    logger: LoggerLike | None = None,
    etc: str | None = None,
    zsh: str | None = None,
    home: PathLike = HOME,
) -> None:
    log_info(logger, "Setting up shell config...")
    match etc, SHELL, zsh:
        case None, "bash" | "posix" | "sh", _:
            path = Path(home, ".bashrc")
            ensure_line(path, bash)
        case None, "zsh", None:
            path = Path(home, ".zshrc")
            ensure_line(path, bash)
        case None, "zsh", str():
            path = Path(home, ".zshrc")
            ensure_line(path, zsh)
        case None, "fish", _:
            path = Path(home, ".config/fish/config.fish")
            ensure_line(path, fish)
        case str(), "bash" | "posix" | "sh", _:
            text = normalize_multi_line_str(f"""
                #!/usr/bin/env sh
                {bash}
            """)
            ensure_line(f"/etc/profile/{etc}.sh", text)
        case str(), _, _:
            msg = f"Invalid shell for 'etc': {repr_str(SHELL)}"
            raise ValueError(msg)
        case never:
            assert_never(never)


##


def setup_ssh_config(
    *,
    logger: LoggerLike | None = None,
    home: PathLike = HOME,
    ssh: str | None = None,
    retry: Retry | None = None,
) -> None:
    """Set up the SSH config."""
    log_info(logger, "Setting up SSH config...")
    config = Path(home, ".ssh/config")
    config_d = Path(home, ".ssh/config.d")
    text = f"Include {config_d}/*.conf"
    if ssh is None:
        write_text(config, text, overwrite=True)
        config_d.mkdir(parents=True, exist_ok=True)
    else:
        user, hostname = split_ssh(ssh)
        cmds: list[list[str]] = [mkdir_cmd(config, parent=True), mkdir_cmd(config_d)]
        utilities.subprocess.ssh(
            user,
            hostname,
            *BASH_LS,
            input="\n".join(map(join, cmds)),
            retry=retry,
            logger=logger,
        )
        utilities.subprocess.ssh(
            user, hostname, *tee_cmd(config), input=text, retry=retry, logger=logger
        )


##


def setup_sshd_config(
    *,
    logger: LoggerLike | None = None,
    permit_root_login: bool = False,
    root: PathLike = FILE_SYSTEM_ROOT,
    ssh: str | None = None,
    sudo: bool = False,
    retry: Retry | None = None,
) -> None:
    log_info(logger, "Setting up SSHD config...")
    path = Path(root, "etc/ssh/sshd_config.d/default.conf")
    text = sshd_config(permit_root_login=permit_root_login)
    if ssh is None:
        tee(path, text, sudo=sudo)
    else:
        user, hostname = split_ssh(ssh)
        path = Path("/etc/ssh/sshd_config.d/default.conf")
        utilities.subprocess.ssh(
            user,
            hostname,
            *maybe_sudo_cmd(*tee_cmd(path), sudo=sudo),
            input=text,
            retry=retry,
            logger=logger,
        )


def sshd_config(*, permit_root_login: bool = False) -> str:
    yes_no = "yes" if permit_root_login else "no"
    return normalize_multi_line_str(f"""
        PasswordAuthentication no
        PermitRootLogin {yes_no}
        PubkeyAcceptedAlgorithms ssh-ed25519
        PubkeyAuthentication yes
    """)


__all__ = [
    "setup_authorized_keys",
    "setup_shell_config",
    "setup_ssh_config",
    "setup_sshd_config",
    "sshd_config",
]
