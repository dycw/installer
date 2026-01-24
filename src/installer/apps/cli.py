from __future__ import annotations

from typing import TYPE_CHECKING

from click import argument, option
from typed_settings import click_options
from utilities.core import is_pytest
from utilities.logging import basic_config

from installer.apps.lib import (
    setup_age,
    setup_apt_package,
    setup_bat,
    setup_bottom,
    setup_curl,
    setup_delta,
    setup_direnv,
    setup_docker,
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
from installer.click import logger_option, retry_option, ssh_option, sudo_option

if TYPE_CHECKING:
    from utilities.types import LoggerLike, Retry


@argument("package", type=str)
@logger_option
@ssh_option
@sudo_option
@retry_option
def apt_package_sub_cmd(
    *,
    package: str,
    logger: LoggerLike | None,
    ssh: str | None,
    sudo: bool,
    retry: Retry | None,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_apt_package(package, logger=logger, ssh=ssh, sudo=sudo, retry=retry)


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
def age_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    ssh: str | None = None,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_age(
        ssh=ssh,
        token=token,
        path_binaries=path_binaries,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
        retry=retry,
        logger=logger,
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
    basic_config(obj=logger)
    setup_bat(
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
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
    basic_config(obj=logger)
    setup_bottom(
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
    )


##


@click_options(SSHSettings, [LOADER], show_envvars_in_help=True, argname="ssh")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def curl_sub_cmd(
    *,
    ssh: str | None = None,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_curl(ssh=ssh, sudo=sudo, retry=retry, logger=logger)


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
    basic_config(obj=logger)
    setup_delta(
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
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
    ssh: str | None = None,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_direnv(
        ssh=ssh,
        path_binaries=path_binaries,
        token=token,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
        etc=etc,
        retry=retry,
        logger=logger,
    )


##


@option("--user", type=str, default=None, help="User to add to the 'docker' group")
@click_options(SSHSettings, [LOADER], show_envvars_in_help=True, argname="ssh")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def docker_sub_cmd(
    *,
    user: str | None,
    ssh: str | None = None,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_docker(ssh=ssh, user=user, sudo=sudo, retry=retry, logger=logger)


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
    basic_config(obj=logger)
    setup_dust(
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
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
    basic_config(obj=logger)
    setup_eza(
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
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
    basic_config(obj=logger)
    setup_fd(
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
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
    ssh: str | None = None,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_fzf(
        ssh=ssh,
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
        etc=etc,
        retry=retry,
        logger=logger,
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
    basic_config(obj=logger)
    setup_jq(
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
    )


##


@click_options(SSHSettings, [LOADER], show_envvars_in_help=True, argname="ssh")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def git_sub_cmd(
    *,
    ssh: str | None = None,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_git(ssh=ssh, sudo=sudo, retry=retry, logger=logger)


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
    ssh: str | None = None,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_just(
        ssh=ssh,
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
        retry=retry,
        logger=logger,
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
    basic_config(obj=logger)
    setup_neovim(
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
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
    ssh: str | None = None,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_restic(
        ssh=ssh,
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
        retry=retry,
        logger=logger,
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
    basic_config(obj=logger)
    setup_ripgrep(
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
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
    basic_config(obj=logger)
    setup_ruff(
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
    )


##


@click_options(SSHSettings, [LOADER], show_envvars_in_help=True, argname="ssh")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def rsync_sub_cmd(
    *,
    ssh: str | None = None,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_rsync(ssh=ssh, sudo=sudo, retry=retry, logger=logger)


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
    basic_config(obj=logger)
    setup_sd(
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
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
    basic_config(obj=logger)
    setup_shellcheck(
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
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
    basic_config(obj=logger)
    setup_shfmt(
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
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
    ssh: str | None = None,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_sops(
        ssh=ssh,
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
        retry=retry,
        logger=logger,
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
    ssh: str | None = None,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_starship(
        ssh=ssh,
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
        etc=etc,
        retry=retry,
        logger=logger,
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
    basic_config(obj=logger)
    setup_taplo(
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
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
    ssh: str | None = None,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_uv(
        ssh=ssh,
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
        retry=retry,
        logger=logger,
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
    basic_config(obj=logger)
    setup_watchexec(
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
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
    basic_config(obj=logger)
    setup_yq(
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
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
    ssh: str | None = None,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_zoxide(
        ssh=ssh,
        token=token,
        timeout=DOWNLOAD_TIMEOUT,
        path_binaries=path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
        etc=etc,
        retry=retry,
        logger=logger,
    )


__all__ = [
    "age_sub_cmd",
    "apt_package_sub_cmd",
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
