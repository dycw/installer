from __future__ import annotations

from pathlib import Path
from shlex import join
from typing import TYPE_CHECKING

import utilities.subprocess
from utilities.atomicwrites import writer
from utilities.subprocess import BASH_LS, maybe_sudo_cmd, mkdir_cmd, tee, tee_cmd
from utilities.tabulate import func_param_desc
from utilities.text import strip_and_dedent

from installer import __version__
from installer.configs.constants import RELATIVE_HOME
from installer.configs.settings import ROOT_SETTINGS, SSHD_SETTINGS
from installer.logging import LOGGER
from installer.settings import SSH_SETTINGS, SUDO_SETTINGS
from installer.utilities import get_home, split_ssh

if TYPE_CHECKING:
    from utilities.types import LoggerLike, PathLike, Retry


def setup_authorized_keys(
    keys: list[str],
    /,
    *,
    ssh: str | None = SSH_SETTINGS.ssh,
    root: PathLike = ROOT_SETTINGS.root,
    retry: Retry | None = SSH_SETTINGS.retry,
    logger: LoggerLike | None = SSH_SETTINGS.logger,
) -> None:
    LOGGER.info(
        func_param_desc(
            setup_authorized_keys,
            __version__,
            f"{keys=}",
            f"{ssh=}",
            f"{root=}",
            f"{retry=}",
            f"{logger=}",
        )
    )
    text = "\n".join(keys)
    if ssh is None:
        home = Path(root, RELATIVE_HOME)
        dest = home / ".ssh/authorized_keys"
        with writer(dest, overwrite=True) as temp:
            _ = temp.write_text(text)
    else:
        user, hostname = split_ssh(ssh)
        home = get_home(ssh=ssh, retry=retry, logger=logger)
        dest = home / ".ssh/authorized_keys"
        utilities.subprocess.ssh(
            user, hostname, *tee_cmd(dest), input=text, retry=retry, logger=logger
        )


##


def setup_ssh_config(
    *,
    ssh: str | None = SSH_SETTINGS.ssh,
    root: PathLike = ROOT_SETTINGS.root,
    retry: Retry | None = SSH_SETTINGS.retry,
    logger: LoggerLike | None = SSH_SETTINGS.logger,
) -> None:
    LOGGER.info(
        func_param_desc(
            setup_ssh_config,
            __version__,
            f"{ssh=}",
            f"{root=}",
            f"{retry=}",
            f"{logger=}",
        )
    )
    if ssh is None:
        home = Path(root, RELATIVE_HOME)
        config = home / ".ssh/config"
        config_d = home / ".ssh/config.d"
        config_d.mkdir(parents=True, exist_ok=True)
        text = f"Include {config_d}/*.conf"
        with writer(config, overwrite=True) as temp:
            _ = temp.write_text(text)
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
        text = f"Include {config_d}/*.conf"
        utilities.subprocess.ssh(
            user, hostname, *tee_cmd(config), input=text, retry=retry, logger=logger
        )


##


def setup_sshd_config(
    *,
    permit_root_login: bool = SSHD_SETTINGS.permit_root_login,
    ssh: str | None = SSH_SETTINGS.ssh,
    root: PathLike = ROOT_SETTINGS.root,
    sudo: bool = SUDO_SETTINGS.sudo,
    retry: Retry | None = SSH_SETTINGS.retry,
    logger: LoggerLike | None = SSH_SETTINGS.logger,
) -> None:
    LOGGER.info(
        func_param_desc(
            setup_sshd_config,
            __version__,
            f"{permit_root_login=}",
            f"{ssh=}",
            f"{root=}",
            f"{retry=}",
            f"{logger=}",
            f"{sudo=}",
        )
    )
    text = sshd_config(permit_root_login=permit_root_login)
    if ssh is None:
        path = Path(root, "etc/ssh/sshd_config.d/default.conf")
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
    return strip_and_dedent(f"""
        PasswordAuthentication no
        PermitRootLogin {yes_no}
        PubkeyAcceptedAlgorithms ssh-ed25519
        PubkeyAuthentication yes
    """)


__all__ = [
    "setup_authorized_keys",
    "setup_ssh_config",
    "setup_sshd_config",
    "sshd_config",
]
