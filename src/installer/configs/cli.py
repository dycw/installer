from __future__ import annotations

from click import argument
from typed_settings import click_options
from utilities.logging import basic_config
from utilities.os import is_pytest

from installer.configs.lib import (
    setup_authorized_keys,
    setup_ssh_config,
    setup_sshd_config,
)
from installer.configs.settings import RootSettings, SSHDSettings
from installer.logging import LOGGER
from installer.settings import LOADER, SSHSettings, SudoSettings


@argument("keys", type=str, nargs=-1)
@click_options(RootSettings, [LOADER], show_envvars_in_help=True, argname="root")
@click_options(SSHSettings, [LOADER], show_envvars_in_help=True, argname="ssh")
def setup_authorized_keys_sub_cmd(
    keys: tuple[str, ...], /, *, root: RootSettings, ssh: SSHSettings
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_authorized_keys(
        list(keys), ssh=ssh.ssh, root=root.root, retry=ssh.retry, logger=ssh.logger
    )


@click_options(RootSettings, [LOADER], show_envvars_in_help=True, argname="root")
@click_options(SSHSettings, [LOADER], show_envvars_in_help=True, argname="ssh")
def setup_ssh_config_sub_cmd(*, root: RootSettings, ssh: SSHSettings) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_ssh_config(ssh=ssh.ssh, root=root.root, retry=ssh.retry, logger=ssh.logger)


@click_options(RootSettings, [LOADER], show_envvars_in_help=True, argname="root")
@click_options(SSHSettings, [LOADER], show_envvars_in_help=True, argname="ssh")
@click_options(SSHDSettings, [LOADER], show_envvars_in_help=True, argname="sshd")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def setup_sshd_sub_cmd(
    *, root: RootSettings, ssh: SSHSettings, sshd: SSHDSettings, sudo: SudoSettings
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_sshd_config(
        permit_root_login=sshd.permit_root_login,
        ssh=ssh.ssh,
        root=root.root,
        sudo=sudo.sudo,
        retry=ssh.retry,
        logger=ssh.logger,
    )


__all__ = [
    "setup_authorized_keys_sub_cmd",
    "setup_ssh_config_sub_cmd",
    "setup_sshd_sub_cmd",
]
