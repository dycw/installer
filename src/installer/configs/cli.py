from __future__ import annotations

from typing import TYPE_CHECKING

from click import argument, option
from utilities.core import is_pytest
from utilities.logging import basic_config

from installer.click import logger_option, retry_option, ssh_option, sudo_option
from installer.configs.lib import (
    setup_authorized_keys,
    setup_ssh_config,
    setup_sshd_config,
)

if TYPE_CHECKING:
    from utilities.types import LoggerLike, Retry


@argument("keys", type=str, nargs=-1)
@logger_option
@ssh_option
@option("--batch-mode", is_flag=True, default=None, help="SSH batch mode")
@retry_option
def setup_authorized_keys_sub_cmd(
    *,
    keys: tuple[str, ...],
    logger: LoggerLike,
    ssh: str | None,
    batch_mode: bool,
    retry: Retry | None,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_authorized_keys(
        list(keys), logger=logger, ssh=ssh, batch_mode=batch_mode, retry=retry
    )


@logger_option
@ssh_option
@retry_option
def setup_ssh_config_sub_cmd(
    *, logger: LoggerLike, ssh: str | None, retry: Retry | None
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_ssh_config(logger=logger, ssh=ssh, retry=retry)


@logger_option
@option("--permit-root-login", is_flag=True, default=False, help="Permit root login")
@ssh_option
@sudo_option
@retry_option
def setup_sshd_sub_cmd(
    *,
    logger: LoggerLike,
    permit_root_login: bool,
    ssh: str | None,
    sudo: bool,
    retry: Retry | None,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_sshd_config(
        logger=logger,
        permit_root_login=permit_root_login,
        ssh=ssh,
        sudo=sudo,
        retry=retry,
    )


__all__ = [
    "setup_authorized_keys_sub_cmd",
    "setup_ssh_config_sub_cmd",
    "setup_sshd_sub_cmd",
]
