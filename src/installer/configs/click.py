from __future__ import annotations

from click import option

etc_option = option(
    "--etc",
    is_flag=True,
    default=False,
    help="Set up in '/etc/profile.d/*.sh' instead of '~/.{bash,zsh}rc'",
)


__all__ = ["etc_option"]
