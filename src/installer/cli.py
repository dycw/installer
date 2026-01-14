from __future__ import annotations

from click import group
from utilities.click import CONTEXT_SETTINGS

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
    yq_sub_cmd,
    zoxide_sub_cmd,
)
from installer.configs.cli import (
    setup_authorized_keys_sub_cmd,
    setup_ssh_config_sub_cmd,
    setup_sshd_sub_cmd,
)


@group(**CONTEXT_SETTINGS)
def _main() -> None: ...


_ = _main.command(name="age", **CONTEXT_SETTINGS)(age_sub_cmd)
_ = _main.command(name="bat", **CONTEXT_SETTINGS)(bat_sub_cmd)
_ = _main.command(name="btm", **CONTEXT_SETTINGS)(bottom_sub_cmd)
_ = _main.command(name="curl", **CONTEXT_SETTINGS)(curl_sub_cmd)
_ = _main.command(name="delta", **CONTEXT_SETTINGS)(delta_sub_cmd)
_ = _main.command(name="direnv", **CONTEXT_SETTINGS)(direnv_sub_cmd)
_ = _main.command(name="dust", **CONTEXT_SETTINGS)(dust_sub_cmd)
_ = _main.command(name="eza", **CONTEXT_SETTINGS)(eza_sub_cmd)
_ = _main.command(name="fd", **CONTEXT_SETTINGS)(fd_sub_cmd)
_ = _main.command(name="fzf", **CONTEXT_SETTINGS)(fzf_sub_cmd)
_ = _main.command(name="jq", **CONTEXT_SETTINGS)(jq_sub_cmd)
_ = _main.command(name="git", **CONTEXT_SETTINGS)(git_sub_cmd)
_ = _main.command(name="just", **CONTEXT_SETTINGS)(just_sub_cmd)
_ = _main.command(name="neovim", **CONTEXT_SETTINGS)(neovim_sub_cmd)
_ = _main.command(name="restic", **CONTEXT_SETTINGS)(restic_sub_cmd)
_ = _main.command(name="ripgrep", **CONTEXT_SETTINGS)(ripgrep_sub_cmd)
_ = _main.command(name="ruff", **CONTEXT_SETTINGS)(ruff_sub_cmd)
_ = _main.command(name="rsync", **CONTEXT_SETTINGS)(rsync_sub_cmd)
_ = _main.command(name="sd", **CONTEXT_SETTINGS)(sd_sub_cmd)
_ = _main.command(name="shellcheck", **CONTEXT_SETTINGS)(shellcheck_sub_cmd)
_ = _main.command(name="shfmt", **CONTEXT_SETTINGS)(shfmt_sub_cmd)
_ = _main.command(name="sops", **CONTEXT_SETTINGS)(sops_sub_cmd)
_ = _main.command(name="starship", **CONTEXT_SETTINGS)(starship_sub_cmd)
_ = _main.command(name="taplo", **CONTEXT_SETTINGS)(taplo_sub_cmd)
_ = _main.command(name="uv", **CONTEXT_SETTINGS)(uv_sub_cmd)
_ = _main.command(name="yq", **CONTEXT_SETTINGS)(yq_sub_cmd)
_ = _main.command(name="zoxide", **CONTEXT_SETTINGS)(zoxide_sub_cmd)


_ = _main.command(name="setup-authorized-keys", **CONTEXT_SETTINGS)(
    setup_authorized_keys_sub_cmd
)
_ = _main.command(name="setup-ssh-config", **CONTEXT_SETTINGS)(setup_ssh_config_sub_cmd)
_ = _main.command(name="setup-sshd-config", **CONTEXT_SETTINGS)(setup_sshd_sub_cmd)


if __name__ == "__main__":
    _main()
