from __future__ import annotations

from re import IGNORECASE, search
from typing import TYPE_CHECKING, Any

from github import Github
from github.Auth import Token
from requests import get
from typed_settings import Secret
from utilities.inflect import counted_noun
from utilities.iterables import OneNonUniqueError, one
from utilities.subprocess import chmod
from utilities.text import strip_and_dedent

from github_downloader import __version__
from github_downloader.constants import MACHINE_TYPE, SYSTEM_NAME
from github_downloader.logging import LOGGER
from github_downloader.settings import AGE_SETTINGS, SETTINGS, SOPS_SETTINGS

if TYPE_CHECKING:
    from pathlib import Path

    from typed_settings import Secret


def setup_asset(
    owner: str,
    repo: str,
    binary_name: str,
    /,
    *,
    token: Secret[str] | None = SETTINGS.token,
    match_system: bool = SETTINGS.match_system,
    match_machine: bool = SETTINGS.match_machine,
    not_endswith: list[str] = SETTINGS.not_endswith,
    timeout: int = SETTINGS.timeout,
    path_binaries: Path = SETTINGS.path_binaries,
    chunk_size: int = SETTINGS.chunk_size,
    permissions: str = SETTINGS.permissions,
) -> None:
    """Download a GitHub release."""
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - owner         = %s
             - repo          = %s
             - binary_name   = %s
             - token         = %s
             - match_system  = %s
             - match_machine = %s
             - not_endswith  = %s
             - timeout       = %s
             - path_binaries = %s
             - chunk_size    = %s
             - permissions   = %s
        """),
        setup_asset.__name__,
        __version__,
        owner,
        repo,
        binary_name,
        token,
        match_system,
        match_machine,
        not_endswith,
        timeout,
        path_binaries,
        chunk_size,
        permissions,
    )
    if SYSTEM_NAME not in {"Darwin", "Linux"}:
        msg = f"Invalid system {SYSTEM_NAME!r}"
        raise ValueError(msg)
    gh = Github(auth=None if token is None else Token(token.get_secret_value()))
    repository = gh.get_repo(f"{owner}/{repo}")
    release = repository.get_latest_release()
    assets = list(release.get_assets())
    LOGGER.info("Got %s: %s", counted_noun(assets, "asset"), [a.name for a in assets])
    if match_system:
        assets = [a for a in assets if search(SYSTEM_NAME, a.name, flags=IGNORECASE)]
        LOGGER.info(
            "Post system name, got %s: %s",
            counted_noun(assets, "asset"),
            [a.name for a in assets],
        )
    if match_machine:
        assets = [a for a in assets if search(MACHINE_TYPE, a.name, flags=IGNORECASE)]
        LOGGER.info(
            "Post machine type %r, got %s: %s",
            counted_noun(assets, "asset"),
            [a.name for a in assets],
        )
    if len(not_endswith) >= 1:
        assets = [
            a for a in assets if all(not a.name.endswith(e) for e in not_endswith)
        ]
        LOGGER.info(
            "Post asset name endings, got %s: %s",
            counted_noun(assets, "asset"),
            [a.name for a in assets],
        )
    try:
        asset = one(assets)
    except OneNonUniqueError as error:
        raise OneNonUniqueError(
            iterables=([a.name for a in assets],),
            first=error.first.name,
            second=error.second.name,
        ) from None
    headers: dict[str, Any] = {}
    if token is not None:
        headers["Authorization"] = f"Bearer {token.get_secret_value()}"
    with get(
        asset.browser_download_url, headers=headers, timeout=timeout, stream=True
    ) as resp:
        resp.raise_for_status()
        path_binaries.mkdir(parents=True, exist_ok=True)
        path_bin = path_binaries / binary_name
        with path_bin.open(mode="wb") as fh:
            fh.writelines(resp.iter_content(chunk_size=chunk_size))
    chmod(path_bin, permissions)
    LOGGER.info("Downloaded to %r", str(path_bin))


def setup_age(
    *,
    binary_name: str = AGE_SETTINGS.binary_name,
    token: Secret[str] | None = AGE_SETTINGS.token,
    timeout: int = AGE_SETTINGS.timeout,
    path_binaries: Path = AGE_SETTINGS.path_binaries,
    chunk_size: int = AGE_SETTINGS.chunk_size,
    permissions: str = AGE_SETTINGS.permissions,
) -> None:
    """Download 'age'."""
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - binary_name   = %s
             - token         = %s
             - timeout       = %s
             - path_binaries = %s
             - chunk_size    = %s
             - permissions   = %s
        """),
        setup_age.__name__,
        __version__,
        binary_name,
        token,
        timeout,
        path_binaries,
        chunk_size,
        permissions,
    )
    setup_asset(
        "FiloSottile",
        "age",
        binary_name,
        token=token,
        match_system=True,
        match_machine=True,
        not_endswith=["proof"],
        timeout=timeout,
        path_binaries=path_binaries,
        chunk_size=chunk_size,
        permissions=permissions,
    )


def setup_sops(
    *,
    binary_name: str = SOPS_SETTINGS.binary_name,
    token: Secret[str] | None = SOPS_SETTINGS.token,
    timeout: int = SOPS_SETTINGS.timeout,
    path_binaries: Path = SOPS_SETTINGS.path_binaries,
    chunk_size: int = SOPS_SETTINGS.chunk_size,
    permissions: str = SOPS_SETTINGS.permissions,
) -> None:
    """Download 'sops'."""
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - binary_name   = %s
             - token         = %s
             - timeout       = %s
             - path_binaries = %s
             - chunk_size    = %s
             - permissions   = %s
        """),
        setup_sops.__name__,
        __version__,
        binary_name,
        token,
        timeout,
        path_binaries,
        chunk_size,
        permissions,
    )
    setup_asset(
        "getsops",
        "sops",
        binary_name,
        token=token,
        match_system=True,
        match_machine=True,
        not_endswith=["json"],
        timeout=timeout,
        path_binaries=path_binaries,
        chunk_size=chunk_size,
        permissions=permissions,
    )


__all__ = ["setup_age", "setup_asset", "setup_sops"]
