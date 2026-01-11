from __future__ import annotations

from click import argument, group
from typed_settings import click_options
from utilities.click import CONTEXT_SETTINGS
from utilities.logging import basic_config
from utilities.os import is_pytest

from github_downloader.lib import (
    setup_age,
    setup_asset,
    setup_bottom,
    setup_direnv,
    setup_fzf,
    setup_git,
    setup_just,
    setup_restic,
    setup_ripgrep,
    setup_sops,
    setup_starship,
)
from github_downloader.logging import LOGGER
from github_downloader.settings import (
    LOADER,
    DownloadSettings,
    EtcSettings,
    MatchSettings,
    PathBinariesSettings,
    PermsSettings,
    SudoSettings,
)


@group(**CONTEXT_SETTINGS)
def _main() -> None: ...


@_main.command(name="run", **CONTEXT_SETTINGS)
@argument("asset-owner", type=str)
@argument("asset-repo", type=str)
@argument("binary-name", type=str)
@click_options(MatchSettings, [LOADER], show_envvars_in_help=True, argname="common")
@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def run_sub_cmd(
    *,
    asset_owner: str,
    asset_repo: str,
    binary_name: str,
    common: MatchSettings,
    download: DownloadSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_asset(
        asset_owner,
        asset_repo,
        binary_name,
        token=download.token,
        match_system=common.match_system,
        match_c_std_lib=common.match_c_std_lib,
        match_machine=common.match_machine,
        not_endswith=common.not_endswith,
        timeout=download.timeout,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
    )


@_main.command(name="age", **CONTEXT_SETTINGS)
@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def age_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_age(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
    )


@_main.command(name="btm", **CONTEXT_SETTINGS)
@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def btm_sub_cmd(
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


@_main.command(name="direnv", **CONTEXT_SETTINGS)
@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(EtcSettings, [LOADER], show_envvars_in_help=True, argname="etc")
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def direnv_sub_cmd(
    *,
    download: DownloadSettings,
    etc: EtcSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_direnv(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
        etc=etc.etc,
    )


@_main.command(name="fzf", **CONTEXT_SETTINGS)
@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(EtcSettings, [LOADER], show_envvars_in_help=True, argname="etc")
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def fzf_sub_cmd(
    *,
    download: DownloadSettings,
    etc: EtcSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_fzf(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
        etc=etc.etc,
    )


@_main.command(name="git", **CONTEXT_SETTINGS)
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def git_sub_cmd(*, sudo: SudoSettings) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_git(sudo=sudo.sudo)


@_main.command(name="just", **CONTEXT_SETTINGS)
@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def just_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_just(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
    )


@_main.command(name="restic", **CONTEXT_SETTINGS)
@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def restic_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_restic(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
    )


@_main.command(name="ripgrep", **CONTEXT_SETTINGS)
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


@_main.command(name="sops", **CONTEXT_SETTINGS)
@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def sops_sub_cmd(
    *,
    download: DownloadSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_sops(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
    )


@_main.command(name="starship", **CONTEXT_SETTINGS)
@click_options(
    DownloadSettings, [LOADER], show_envvars_in_help=True, argname="download"
)
@click_options(EtcSettings, [LOADER], show_envvars_in_help=True, argname="etc")
@click_options(
    PathBinariesSettings, [LOADER], show_envvars_in_help=True, argname="path_binaries"
)
@click_options(PermsSettings, [LOADER], show_envvars_in_help=True, argname="perms")
@click_options(SudoSettings, [LOADER], show_envvars_in_help=True, argname="sudo")
def starship_sub_cmd(
    *,
    download: DownloadSettings,
    etc: EtcSettings,
    path_binaries: PathBinariesSettings,
    perms: PermsSettings,
    sudo: SudoSettings,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_starship(
        token=download.token,
        timeout=download.timeout,
        path_binaries=path_binaries.path_binaries,
        chunk_size=download.chunk_size,
        sudo=sudo.sudo,
        perms=perms.perms,
        owner=perms.owner,
        group=perms.group,
        etc=etc.etc,
    )


if __name__ == "__main__":
    _main()
