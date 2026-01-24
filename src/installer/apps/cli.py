from __future__ import annotations

from typing import TYPE_CHECKING

from click import argument, option
from utilities.core import PermissionsLike, is_pytest
from utilities.logging import basic_config

from installer.apps.click import (
    group_option,
    owner_option,
    path_binaries_option,
    perms_option,
    token_option,
)
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
from installer.configs.click import etc_option

if TYPE_CHECKING:
    from utilities.pydantic import SecretLike
    from utilities.types import LoggerLike, PathLike, Retry


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


@logger_option
@ssh_option
@token_option
@path_binaries_option
@sudo_option
@perms_option
@owner_option
@group_option
@retry_option
def age_sub_cmd(
    *,
    logger: LoggerLike | None,
    ssh: str | None,
    token: SecretLike | None,
    path_binaries: PathLike,
    sudo: bool,
    perms: PermissionsLike | None,
    owner: str | int | None,
    group: str | int | None,
    retry: Retry | None,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_age(
        logger=logger,
        ssh=ssh,
        token=token,
        path_binaries=path_binaries,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
        retry=retry,
    )


##


@logger_option
@token_option
@path_binaries_option
@sudo_option
@perms_option
@owner_option
@group_option
def bat_sub_cmd(
    *,
    logger: LoggerLike | None,
    token: SecretLike | None,
    path_binaries: PathLike,
    sudo: bool,
    perms: PermissionsLike | None,
    owner: str | int | None,
    group: str | int | None,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_bat(
        logger=logger,
        token=token,
        path_binaries=path_binaries,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
    )


##


@logger_option
@token_option
@path_binaries_option
@sudo_option
@perms_option
@owner_option
@group_option
def bottom_sub_cmd(
    *,
    logger: LoggerLike | None,
    token: SecretLike | None,
    path_binaries: PathLike,
    sudo: bool,
    perms: PermissionsLike | None,
    owner: str | int | None,
    group: str | int | None,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_bottom(
        logger=logger,
        token=token,
        path_binaries=path_binaries,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
    )


##


@logger_option
@ssh_option
@sudo_option
@retry_option
def curl_sub_cmd(
    *, logger: LoggerLike | None, ssh: str | None, sudo: bool, retry: Retry | None
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_curl(logger=logger, ssh=ssh, sudo=sudo, retry=retry)


##


@logger_option
@token_option
@path_binaries_option
@sudo_option
@perms_option
@owner_option
@group_option
@retry_option
def delta_sub_cmd(
    *,
    logger: LoggerLike | None,
    token: SecretLike | None,
    path_binaries: PathLike,
    sudo: bool,
    perms: PermissionsLike | None,
    owner: str | int | None,
    group: str | int | None,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_delta(
        logger=logger,
        token=token,
        path_binaries=path_binaries,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
    )


##


@logger_option
@ssh_option
@path_binaries_option
@token_option
@sudo_option
@perms_option
@owner_option
@group_option
@etc_option
@retry_option
def direnv_sub_cmd(
    *,
    logger: LoggerLike | None,
    ssh: str | None,
    path_binaries: PathLike,
    token: SecretLike | None,
    sudo: bool,
    perms: PermissionsLike | None,
    owner: str | int | None,
    group: str | int | None,
    etc: bool,
    retry: Retry | None,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_direnv(
        logger=logger,
        ssh=ssh,
        path_binaries=path_binaries,
        token=token,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
        etc=etc,
        retry=retry,
    )


##


@logger_option
@ssh_option
@sudo_option
@option("--user", type=str, default=None, help="User to add to the 'docker' group")
@retry_option
def docker_sub_cmd(
    *,
    logger: LoggerLike | None = None,
    ssh: str | None = None,
    sudo: bool = False,
    user: str | None = None,
    retry: Retry | None = None,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_docker(logger=logger, ssh=ssh, sudo=sudo, user=user, retry=retry)


##


@logger_option
@token_option
@path_binaries_option
@sudo_option
@perms_option
@owner_option
@group_option
def dust_sub_cmd(
    *,
    logger: LoggerLike | None,
    token: SecretLike | None,
    path_binaries: PathLike,
    sudo: bool,
    perms: PermissionsLike | None,
    owner: str | int | None,
    group: str | int | None,
) -> None:
    if is_pytest():
        return
    basic_config(obj=logger)
    setup_dust(
        logger=logger,
        token=token,
        path_binaries=path_binaries,
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
