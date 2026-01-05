from __future__ import annotations

from click import group
from rich.pretty import pretty_repr
from typed_settings import click_options
from utilities.click import CONTEXT_SETTINGS
from utilities.logging import basic_config
from utilities.os import is_pytest

from github_downloader.lib import download_release
from github_downloader.logging import LOGGER
from github_downloader.settings import LOADER, Settings


@group(**CONTEXT_SETTINGS)
def _main() -> None: ...


@_main.command(name="run", **CONTEXT_SETTINGS)
@click_options(Settings, [LOADER], show_envvars_in_help=True)
def run_sub_cmd(settings: Settings, /) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    LOGGER.info("Settings = %s", pretty_repr(settings))
    download_release(
        settings.owner,
        settings.repo,
        settings.binary_name,
        token=settings.token,
        match_system=settings.match_system,
        system_name=settings.system_name,
        match_machine=settings.match_machine,
        machine_type=settings.machine_type,
        not_endswith=settings.not_endswith,
        timeout=settings.timeout,
        path_binaries=settings.path_binaries,
        chunk_size=settings.chunk_size,
        permissions=settings.permissions,
    )


if __name__ == "__main__":
    _main()
