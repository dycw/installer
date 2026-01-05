from __future__ import annotations

from click import argument, group
from rich.pretty import pretty_repr
from typed_settings import click_options
from utilities.click import CONTEXT_SETTINGS
from utilities.logging import basic_config
from utilities.os import is_pytest

from github_downloader.lib import download_release, download_sops
from github_downloader.logging import LOGGER
from github_downloader.settings import LOADER, Settings, SopsSettings


@group(**CONTEXT_SETTINGS)
def _main() -> None: ...


@_main.command(name="run", **CONTEXT_SETTINGS)
@argument("owner", type=str)
@argument("repo", type=str)
@argument("binary-name", type=str)
@click_options(Settings, [LOADER], show_envvars_in_help=True)
def run_sub_cmd(
    settings: Settings, /, *, owner: str, repo: str, binary_name: str
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    LOGGER.info("Settings = %s", pretty_repr(settings))
    download_release(
        owner,
        repo,
        binary_name,
        token=settings.token,
        match_system=settings.match_system,
        match_machine=settings.match_machine,
        not_endswith=settings.not_endswith,
        timeout=settings.timeout,
        path_binaries=settings.path_binaries,
        chunk_size=settings.chunk_size,
        permissions=settings.permissions,
    )


@_main.command(name="sops", **CONTEXT_SETTINGS)
@click_options(SopsSettings, [LOADER], show_envvars_in_help=True)
def sops_sub_cmd(settings: SopsSettings, /) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    LOGGER.info("Settings = %s", pretty_repr(settings))
    download_sops(
        binary_name=settings.binary_name,
        token=settings.token,
        timeout=settings.timeout,
        path_binaries=settings.path_binaries,
        chunk_size=settings.chunk_size,
        permissions=settings.permissions,
    )


if __name__ == "__main__":
    _main()
