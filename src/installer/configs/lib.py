from __future__ import annotations

from pathlib import Path
from shlex import join
from typing import TYPE_CHECKING, assert_never

import utilities.subprocess
from utilities.core import (
    log_info,
    normalize_multi_line_str,
    normalize_str,
    repr_str,
    write_text,
)
from utilities.shellingham import SHELL
from utilities.subprocess import BASH_LS, maybe_sudo_cmd, mkdir_cmd, tee, tee_cmd
from utilities.tabulate import func_param_desc
from xdg_base_dirs import xdg_config_home

from installer import __version__
from installer.constants import FILE_SYSTEM_ROOT, RELATIVE_HOME
from installer.logging import LOGGER
from installer.utilities import ensure_line, get_home, split_ssh

if TYPE_CHECKING:
    from utilities.types import LoggerLike, PathLike, Retry


def setup_authorized_keys(
    keys: list[str],
    /,
    *,
    logger: LoggerLike = LOGGER,
    ssh: str | None = None,
    batch_mode: bool = False,
    retry: Retry | None = None,
    __root: PathLike = FILE_SYSTEM_ROOT,
) -> None:
    """Set up the SSH authorized keys."""
    log_info(
        logger,
        func_param_desc(
            setup_authorized_keys,
            __version__,
            f"{keys=}",
            f"{logger=}",
            f"{ssh=}",
            f"{batch_mode=}",
            f"{retry=}",
        ),
    )
    text = normalize_str("\n".join(keys))
    if ssh is None:
        home = Path(__root, RELATIVE_HOME)
        dest = home / ".ssh/authorized_keys"
        write_text(dest, text, overwrite=True)
    else:
        user, hostname = split_ssh(ssh)
        home = get_home(ssh=ssh, batch_mode=batch_mode, retry=retry, logger=logger)
        dest = home / ".ssh/authorized_keys"
        utilities.subprocess.ssh(
            user,
            hostname,
            *tee_cmd(dest),
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
    etc: str | None = None,
    zsh: str | None = None,
    __root: PathLike = FILE_SYSTEM_ROOT,
) -> None:
    match etc, SHELL, zsh:
        case None, "bash" | "posix" | "sh", _:
            home = Path(__root, RELATIVE_HOME)
            ensure_line(home / ".bashrc", bash)
        case None, "zsh", None:
            home = Path(__root, RELATIVE_HOME)
            ensure_line(home / ".zshrc", bash)
        case None, "zsh", str():
            home = Path(__root, RELATIVE_HOME)
            ensure_line(home / ".zshrc", zsh)
        case None, "fish", _:
            ensure_line(xdg_config_home() / "fish/config.fish", fish)
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
    ssh: str | None = None,
    retry: Retry | None = None,
    logger: LoggerLike = LOGGER,
    __root: PathLike = FILE_SYSTEM_ROOT,
) -> None:
    """Set up the SSH config."""
    log_info(
        logger,
        func_param_desc(
            setup_ssh_config, __version__, f"{ssh=}", f"{retry=}", f"{logger=}"
        ),
    )
    if ssh is None:
        home = Path(__root, RELATIVE_HOME)
        config = home / ".ssh/config"
        config_d = home / ".ssh/config.d"
        config_d.mkdir(parents=True, exist_ok=True)
        text = f"Include {config_d}/*.conf"
        write_text(config, text, overwrite=True)
    else:
        user, hostname = split_ssh(ssh)
        home = get_home(ssh=ssh, retry=retry, logger=logger)
        config = home / ".ssh/config"
        config_d = home / ".ssh/config.d"
        cmds: list[list[str]] = [mkdir_cmd(config, parent=True), mkdir_cmd(config_d)]
        utilities.subprocess.ssh(
            user,
            hostname,
            *BASH_LS,
            input="\n".join(map(join, cmds)),
            retry=retry,
            logger=logger,
        )
        text = f"Include {config_d}/*.conf\n"
        utilities.subprocess.ssh(
            user, hostname, *tee_cmd(config), input=text, retry=retry, logger=logger
        )


##


def setup_sshd_config(
    *,
    permit_root_login: bool = SSHD_SETTINGS.permit_root_login,
    ssh: str | None = None,
    sudo: bool = False,
    retry: Retry | None = None,
    logger: LoggerLike = LOGGER,
    __root: PathLike = FILE_SYSTEM_ROOT,
) -> None:
    log_info(
        logger,
        func_param_desc(
            setup_sshd_config,
            __version__,
            f"{permit_root_login=}",
            f"{ssh=}",
            f"{retry=}",
            f"{logger=}",
            f"{sudo=}",
        ),
    )
    text = sshd_config(permit_root_login=permit_root_login)
    if ssh is None:
        path = Path(__root, "etc/ssh/sshd_config.d/default.conf")
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


def sshd_config(*, permit_root_login: bool = SSHD_SETTINGS.permit_root_login) -> str:
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
