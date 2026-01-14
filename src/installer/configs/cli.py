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
from installer.configs.settings import SSHDSettings
from installer.logging import LOGGER
from installer.settings import SudoSettings
from installer.utilities import LOADER


@argument("keys", type=str, nargs=-1)
def setup_authorized_keys_sub_cmd(keys: tuple[str, ...]) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_authorized_keys(list(keys))


def setup_ssh_config_sub_cmd() -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_ssh_config()


@click_options(SSHDSettings, [LOADER], show_envvars_in_help=True, argname="sshd")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def setup_sshd_sub_cmd(*, sshd: SSHDSettings, sudo: SudoSettings) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_sshd_config(permit_root_login=sshd.permit_root_login, sudo=sudo.sudo)


__all__ = [
    "setup_authorized_keys_sub_cmd",
    "setup_ssh_config_sub_cmd",
    "setup_sshd_sub_cmd",
]
