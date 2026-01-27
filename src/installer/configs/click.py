from __future__ import annotations

from click import option
from utilities.click import Path
from utilities.constants import HOME

from installer.configs.constants import FILE_SYSTEM_ROOT

etc_option = option(
    "--etc",
    is_flag=True,
    default=False,
    help="Set up in '/etc/profile.d/*.sh' instead of '~/.{bash,zsh}rc'",
)
home_option = option(
    "--home",
    type=Path(exist="dir if exists"),
    default=HOME,
    help="Path to the home directory",
)
permit_root_login_option = option(
    "--permit-root-login", is_flag=True, default=False, help="Permit root login"
)
root_option = option(
    "--root",
    type=Path(exist="dir if exists"),
    default=FILE_SYSTEM_ROOT,
    help="File system root",
)


__all__ = ["etc_option", "home_option", "permit_root_login_option", "root_option"]
