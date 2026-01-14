from __future__ import annotations

from typed_settings import click_options
from utilities.logging import basic_config
from utilities.os import is_pytest

from installer.configs.lib import setup_ssh, setup_sshd
from installer.configs.settings import SSHDSettings
from installer.logging import LOGGER
from installer.settings import SudoSettings
from installer.utilities import LOADER


def setup_ssh_sub_cmd() -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_ssh()


@click_options(SSHDSettings, [LOADER], show_envvars_in_help=True, argname="sshd")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def setup_sshd_sub_cmd(*, sshd: SSHDSettings, sudo: SudoSettings) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_sshd(permit_root_login=sshd.permit_root_login, sudo=sudo.sudo)


__all__ = ["setup_ssh_sub_cmd", "setup_sshd_sub_cmd"]
