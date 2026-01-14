from __future__ import annotations

from typing import TYPE_CHECKING

from utilities.atomicwrites import writer
from utilities.tabulate import func_param_desc

from installer import __version__
from installer.configs.constants import SSH
from installer.logging import LOGGER

if TYPE_CHECKING:
    from pathlib import Path


def setup_ssh_config() -> None:
    LOGGER.info(func_param_desc(setup_ssh_config, __version__))
    path = _get_ssh_config("*")
    with writer(SSH / "config", overwrite=True) as temp:
        _ = temp.write_text(f"Include {path}")
    path.parent.mkdir(parents=True, exist_ok=True)


def _get_ssh_config(stem: str, /) -> Path:
    return SSH / "config.d" / f"{stem}.conf"


__all__ = ["setup_ssh_config"]
