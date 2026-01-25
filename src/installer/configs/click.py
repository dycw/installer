from __future__ import annotations

from pathlib import Path

import click
from click import option
from utilities.constants import HOME

etc_option = option(
    "--etc",
    is_flag=True,
    default=False,
    help="Set up in '/etc/profile.d/*.sh' instead of '~/.{bash,zsh}rc'",
)
home_option = option(
    "--home",
    type=click.Path(path_type=Path),
    default=HOME,
    help="Path to the home directory",
)
permit_root_login_option = option(
    "--permit-root-login", is_flag=True, default=False, help="Permit root login"
)

__all__ = ["etc_option", "home_option", "permit_root_login_option"]
