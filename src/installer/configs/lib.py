from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from utilities.atomicwrites import writer
from utilities.subprocess import tee
from utilities.tabulate import func_param_desc
from utilities.text import strip_and_dedent

from installer import __version__
from installer.configs.constants import REL_SSH
from installer.configs.settings import SSHD_SETTINGS
from installer.logging import LOGGER
from installer.settings import SUDO_SETTINGS

if TYPE_CHECKING:
    from utilities.types import PathLike


def setup_authorized_keys(keys: list[str], /, *, root: PathLike = "/") -> None:
    LOGGER.info(
        func_param_desc(setup_authorized_keys, __version__, f"{keys=}", f"{root=}")
    )
    root = Path(root)
    with writer(root / REL_SSH / "authorized_keys", overwrite=True) as temp:
        _ = temp.write_text("\n".join(keys))


##


def setup_ssh_config(*, root: PathLike = "/") -> None:
    LOGGER.info(func_param_desc(setup_ssh_config, __version__, f"{root=}"))
    root = Path(root)
    ssh = root / REL_SSH
    path = ssh / "config.d/*.conf"
    with writer(ssh / "config", overwrite=True) as temp:
        _ = temp.write_text(f"Include {path}")
    path.parent.mkdir(parents=True, exist_ok=True)


##


def setup_sshd_config(
    *,
    root: PathLike = "/",
    permit_root_login: bool = SSHD_SETTINGS.permit_root_login,
    sudo: bool = SUDO_SETTINGS.sudo,
) -> None:
    LOGGER.info(
        func_param_desc(
            setup_sshd_config,
            __version__,
            f"{root=}",
            f"{permit_root_login=}",
            f"{sudo=}",
        )
    )
    root = Path(root)
    path = root / "etc/ssh/sshd_config.d/default.conf"
    yes_no = "yes" if permit_root_login else "no"
    text = strip_and_dedent(f"""
        PasswordAuthentication no
        PermitRootLogin ${yes_no}
        PubkeyAcceptedAlgorithms ssh-ed25519
        PubkeyAuthentication yes
    """)
    tee(path, text, sudo=sudo)


__all__ = ["setup_authorized_keys", "setup_ssh_config", "setup_sshd_config"]
