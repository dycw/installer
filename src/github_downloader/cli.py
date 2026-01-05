from __future__ import annotations

from click import argument, group
from rich.pretty import pretty_repr
from typed_settings import click_options
from utilities.click import CONTEXT_SETTINGS
from utilities.logging import basic_config
from utilities.os import is_pytest
from utilities.text import strip_and_dedent

from github_downloader import __version__
from github_downloader.lib import setup_age, setup_asset, setup_sops
from github_downloader.logging import LOGGER
from github_downloader.settings import LOADER, AgeSettings, Settings, SopsSettings


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
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
            %s
        """),
        setup_asset.__name__,
        __version__,
        pretty_repr(settings),
    )
    if settings.token is not None:
        LOGGER.info("Token = %r", settings.token.get_secret_value())
    setup_asset(
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


@_main.command(name="age", **CONTEXT_SETTINGS)
@click_options(AgeSettings, [LOADER], show_envvars_in_help=True)
def age_sub_cmd(settings: AgeSettings, /) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
            %s
        """),
        setup_age.__name__,
        __version__,
        pretty_repr(settings),
    )
    if settings.token is not None:
        LOGGER.info("Token = %r", settings.token.get_secret_value())
    setup_age(
        binary_name=settings.binary_name,
        token=settings.token,
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
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
            %s
        """),
        setup_sops.__name__,
        __version__,
        pretty_repr(settings),
    )
    if settings.token is not None:
        LOGGER.info("Token = %r", settings.token.get_secret_value())
    setup_sops(
        binary_name=settings.binary_name,
        token=settings.token,
        timeout=settings.timeout,
        path_binaries=settings.path_binaries,
        chunk_size=settings.chunk_size,
        permissions=settings.permissions,
    )


if __name__ == "__main__":
    _main()
