from __future__ import annotations

from click import command
from rich.pretty import pretty_repr
from typed_settings import click_options
from utilities.click import CONTEXT_SETTINGS
from utilities.logging import basic_config
from utilities.os import is_pytest

from github_downloader.lib import download_release
from github_downloader.logging import LOGGER
from github_downloader.settings import LOADER, Settings


@command(**CONTEXT_SETTINGS)
@click_options(Settings, [LOADER], show_envvars_in_help=True)
def _main(settings: Settings, /) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    LOGGER.info("Settings = %s", pretty_repr(settings))
    download_release(
        token=settings.token,
        system=settings.system,
        machine=settings.machine,
        path_binary=settings.path_binary,
        timeout=settings.timeout,
        chunk_size=settings.chunk_size,
    )


if __name__ == "__main__":
    _main()
