from __future__ import annotations

from click import group, version_option
from utilities.click import CONTEXT_SETTINGS

from installer import __version__
from installer.apps.cli import (
    age_sub_cmd,
    bat_sub_cmd,
    bottom_sub_cmd,
    curl_sub_cmd,
    delta_sub_cmd,
    direnv_sub_cmd,
    dust_sub_cmd,
    eza_sub_cmd,
    fd_sub_cmd,
    fzf_sub_cmd,
    git_sub_cmd,
    jq_sub_cmd,
    just_sub_cmd,
    neovim_sub_cmd,
    restic_sub_cmd,
    ripgrep_sub_cmd,
    rsync_sub_cmd,
    ruff_sub_cmd,
    sd_sub_cmd,
    shellcheck_sub_cmd,
    shfmt_sub_cmd,
    sops_sub_cmd,
    starship_sub_cmd,
    taplo_sub_cmd,
    uv_sub_cmd,
    watchexec_sub_cmd,
    yq_sub_cmd,
    zoxide_sub_cmd,
)
from installer.clone.cli import git_clone_sub_cmd
from installer.configs.cli import (
    setup_authorized_keys_sub_cmd,
    setup_ssh_config_sub_cmd,
    setup_sshd_sub_cmd,
)


@group(**CONTEXT_SETTINGS)
@version_option(version=__version__)
def cli() -> None: ...


_ = cli.command(name="age", **CONTEXT_SETTINGS)(age_sub_cmd)
_ = cli.command(name="bat", **CONTEXT_SETTINGS)(bat_sub_cmd)
_ = cli.command(name="btm", **CONTEXT_SETTINGS)(bottom_sub_cmd)
_ = cli.command(name="curl", **CONTEXT_SETTINGS)(curl_sub_cmd)
_ = cli.command(name="delta", **CONTEXT_SETTINGS)(delta_sub_cmd)
_ = cli.command(name="direnv", **CONTEXT_SETTINGS)(direnv_sub_cmd)
_ = cli.command(name="dust", **CONTEXT_SETTINGS)(dust_sub_cmd)
_ = cli.command(name="eza", **CONTEXT_SETTINGS)(eza_sub_cmd)
_ = cli.command(name="fd", **CONTEXT_SETTINGS)(fd_sub_cmd)
_ = cli.command(name="fzf", **CONTEXT_SETTINGS)(fzf_sub_cmd)
_ = cli.command(name="jq", **CONTEXT_SETTINGS)(jq_sub_cmd)
_ = cli.command(name="git", **CONTEXT_SETTINGS)(git_sub_cmd)
_ = cli.command(name="just", **CONTEXT_SETTINGS)(just_sub_cmd)
_ = cli.command(name="neovim", **CONTEXT_SETTINGS)(neovim_sub_cmd)
_ = cli.command(name="restic", **CONTEXT_SETTINGS)(restic_sub_cmd)
_ = cli.command(name="ripgrep", **CONTEXT_SETTINGS)(ripgrep_sub_cmd)
_ = cli.command(name="ruff", **CONTEXT_SETTINGS)(ruff_sub_cmd)
_ = cli.command(name="rsync", **CONTEXT_SETTINGS)(rsync_sub_cmd)
_ = cli.command(name="sd", **CONTEXT_SETTINGS)(sd_sub_cmd)
_ = cli.command(name="shellcheck", **CONTEXT_SETTINGS)(shellcheck_sub_cmd)
_ = cli.command(name="shfmt", **CONTEXT_SETTINGS)(shfmt_sub_cmd)
_ = cli.command(name="sops", **CONTEXT_SETTINGS)(sops_sub_cmd)
_ = cli.command(name="starship", **CONTEXT_SETTINGS)(starship_sub_cmd)
_ = cli.command(name="taplo", **CONTEXT_SETTINGS)(taplo_sub_cmd)
_ = cli.command(name="uv", **CONTEXT_SETTINGS)(uv_sub_cmd)
_ = cli.command(name="watchexec", **CONTEXT_SETTINGS)(watchexec_sub_cmd)
_ = cli.command(name="yq", **CONTEXT_SETTINGS)(yq_sub_cmd)
_ = cli.command(name="zoxide", **CONTEXT_SETTINGS)(zoxide_sub_cmd)


_ = cli.command(name="git-clone", **CONTEXT_SETTINGS)(git_clone_sub_cmd)


_ = cli.command(name="setup-authorized-keys", **CONTEXT_SETTINGS)(
    setup_authorized_keys_sub_cmd
)
_ = cli.command(name="setup-ssh-config", **CONTEXT_SETTINGS)(setup_ssh_config_sub_cmd)
_ = cli.command(name="setup-sshd-config", **CONTEXT_SETTINGS)(setup_sshd_sub_cmd)


if __name__ == "__main__":
    cli()
