from __future__ import annotations

from typed_settings import click_options
from utilities.core import is_pytest
from utilities.logging import basic_config

from installer.apps.lib import (
    setup_age,
    setup_bat,
    setup_bottom,
    setup_curl,
    setup_delta,
    setup_direnv,
    setup_dust,
    setup_eza,
    setup_fd,
    setup_fzf,
    setup_git,
    setup_jq,
    setup_just,
    setup_neovim,
    setup_restic,
    setup_ripgrep,
    setup_rsync,
    setup_ruff,
    setup_sd,
    setup_shellcheck,
    setup_shfmt,
    setup_sops,
    setup_starship,
    setup_taplo,
    setup_uv,
    setup_watchexec,
    setup_yq,
    setup_zoxide,
)
from installer.apps.settings import (
    DownloadSettings,
    PathBinariesSettings,
    PermsSettings,
)
from installer.configs.settings import ShellConfigSettings
from installer.logging import LOGGER
from installer.settings import LOADER, SSHSettings, SudoSettings


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SSHSettings, [LOADER], show_envvars_in_help=True, argname="ssh")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def age_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    ssh: SSHSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_age(
        ssh=ssh.ssh,
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
        retry=ssh.retry,
        logger=ssh.logger,
    )


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def bat_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_bat(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
    )


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def bottom_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_bottom(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
    )


##


@click_options(SSHSettings, [LOADER], show_envvars_in_help=True, argname="ssh")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def curl_sub_cmd(*, ssh: SSHSettings, sudo: SudoSettings) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_curl(ssh=ssh.ssh, sudo=sudo.sudo, retry=ssh.retry, logger=ssh.logger)


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def delta_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_delta(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
    )


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(
    ShellConfigSettings, [LOADER], show_envvars_in_help=True, argname="shell_config"
)
@click_options(SSHSettings, [LOADER], show_envvars_in_help=True, argname="ssh")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def direnv_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    shell_config: ShellConfigSettings,
    ssh: SSHSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_direnv(
        ssh=ssh.ssh,
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
        etc=shell_config.etc,
        retry=ssh.retry,
        logger=ssh.logger,
    )


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def dust_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_dust(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
    )


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def eza_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_eza(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
    )


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def fd_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_fd(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
    )


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(
    ShellConfigSettings, [LOADER], show_envvars_in_help=True, argname="shell_config"
)
@click_options(SSHSettings, [LOADER], show_envvars_in_help=True, argname="ssh")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def fzf_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    shell_config: ShellConfigSettings,
    ssh: SSHSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_fzf(
        ssh=ssh.ssh,
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
        etc=shell_config.etc,
        retry=ssh.retry,
        logger=ssh.logger,
    )


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def jq_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_jq(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
    )


##


@click_options(SSHSettings, [LOADER], show_envvars_in_help=True, argname="ssh")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def git_sub_cmd(*, ssh: SSHSettings, sudo: SudoSettings) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_git(ssh=ssh.ssh, sudo=sudo.sudo, retry=ssh.retry, logger=ssh.logger)


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SSHSettings, [LOADER], show_envvars_in_help=True, argname="ssh")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def just_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    ssh: SSHSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_just(
        ssh=ssh.ssh,
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
        retry=ssh.retry,
        logger=ssh.logger,
    )


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def neovim_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_neovim(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
    )


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SSHSettings, [LOADER], show_envvars_in_help=True, argname="ssh")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def restic_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    ssh: SSHSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_restic(
        ssh=ssh.ssh,
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
        retry=ssh.retry,
        logger=ssh.logger,
    )


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def ripgrep_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_ripgrep(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
    )


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def ruff_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_ruff(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
    )


##


@click_options(SSHSettings, [LOADER], show_envvars_in_help=True, argname="ssh")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def rsync_sub_cmd(*, ssh: SSHSettings, sudo: SudoSettings) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_rsync(ssh=ssh.ssh, sudo=sudo.sudo, retry=ssh.retry, logger=ssh.logger)


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def sd_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_sd(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
    )


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def shellcheck_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_shellcheck(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
    )


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def shfmt_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_shfmt(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
    )


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SSHSettings, [LOADER], show_envvars_in_help=True, argname="ssh")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def sops_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    ssh: SSHSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_sops(
        ssh=ssh.ssh,
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
        retry=ssh.retry,
        logger=ssh.logger,
    )


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(
    ShellConfigSettings, [LOADER], show_envvars_in_help=True, argname="shell_config"
)
@click_options(SSHSettings, [LOADER], show_envvars_in_help=True, argname="ssh")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def starship_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    shell_config: ShellConfigSettings,
    ssh: SSHSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_starship(
        ssh=ssh.ssh,
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
        etc=shell_config.etc,
        retry=ssh.retry,
        logger=ssh.logger,
    )


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def taplo_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_taplo(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
    )


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SSHSettings, [LOADER], show_envvars_in_help=True, argname="ssh")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def uv_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    ssh: SSHSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_uv(
        ssh=ssh.ssh,
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
        retry=ssh.retry,
        logger=ssh.logger,
    )


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def watchexec_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_watchexec(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
    )


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def yq_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_yq(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
    )


##


@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(
    ShellConfigSettings, [LOADER], show_envvars_in_help=True, argname="shell_config"
)
@click_options(SSHSettings, [LOADER], show_envvars_in_help=True, argname="ssh")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def zoxide_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    shell_config: ShellConfigSettings,
    ssh: SSHSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_zoxide(
        ssh=ssh.ssh,
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
        etc=shell_config.etc,
        retry=ssh.retry,
        logger=ssh.logger,
    )


__all__ = [
    "age_sub_cmd",
    "bat_sub_cmd",
    "bottom_sub_cmd",
    "curl_sub_cmd",
    "delta_sub_cmd",
    "direnv_sub_cmd",
    "dust_sub_cmd",
    "eza_sub_cmd",
    "fd_sub_cmd",
    "fzf_sub_cmd",
    "git_sub_cmd",
    "jq_sub_cmd",
    "just_sub_cmd",
    "neovim_sub_cmd",
    "restic_sub_cmd",
    "ripgrep_sub_cmd",
    "rsync_sub_cmd",
    "ruff_sub_cmd",
    "sd_sub_cmd",
    "shellcheck_sub_cmd",
    "shfmt_sub_cmd",
    "sops_sub_cmd",
    "starship_sub_cmd",
    "taplo_sub_cmd",
    "uv_sub_cmd",
    "watchexec_sub_cmd",
    "yq_sub_cmd",
    "zoxide_sub_cmd",
]
