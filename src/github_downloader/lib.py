from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from re import IGNORECASE, search
from typing import TYPE_CHECKING, Any

from github import Github
from github.Auth import Token
from requests import get
from typed_settings import Secret
from utilities.inflect import counted_noun
from utilities.iterables import OneNonUniqueError, one
from utilities.subprocess import cp
from utilities.tempfile import TemporaryDirectory
from utilities.text import strip_and_dedent

from github_downloader import __version__
from github_downloader.constants import MACHINE_TYPE_GROUP, SYSTEM_NAME
from github_downloader.logging import LOGGER
from github_downloader.settings import (
    AGE_SETTINGS,
    COMMON_SETTINGS,
    PATH_BINARIES_SETTINGS,
    PERM_SETTINGS,
    SOPS_SETTINGS,
)

if TYPE_CHECKING:
    from collections.abc import Iterator

    from typed_settings import Secret
    from utilities.permissions import PermissionsLike
    from utilities.types import PathLike


@contextmanager
def yield_asset(
    owner: str,
    repo: str,
    /,
    *,
    token: Secret[str] | None = COMMON_SETTINGS.token,
    match_system: bool = COMMON_SETTINGS.match_system,
    match_machine: bool = COMMON_SETTINGS.match_machine,
    not_endswith: list[str] | None = COMMON_SETTINGS.not_endswith,
    timeout: int = COMMON_SETTINGS.timeout,
    chunk_size: int = COMMON_SETTINGS.chunk_size,
) -> Iterator[Path]:
    """Yield a GitHub asset."""
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - owner         = %s
             - repo          = %s
             - token         = %s
             - match_system  = %s
             - match_machine = %s
             - not_endswith  = %s
             - timeout       = %d
             - chunk_size    = %d
        """),
        yield_asset.__name__,
        __version__,
        owner,
        repo,
        token,
        match_system,
        match_machine,
        not_endswith,
        timeout,
        chunk_size,
    )
    gh = Github(auth=None if token is None else Token(token.get_secret_value()))
    repository = gh.get_repo(f"{owner}/{repo}")
    release = repository.get_latest_release()
    assets = list(release.get_assets())
    LOGGER.info("Got %s: %s", counted_noun(assets, "asset"), [a.name for a in assets])
    if match_system:
        assets = [a for a in assets if search(SYSTEM_NAME, a.name, flags=IGNORECASE)]
        LOGGER.info(
            "Post system name %r, got %s: %s",
            SYSTEM_NAME,
            counted_noun(assets, "asset"),
            [a.name for a in assets],
        )
    if match_machine:
        assets = [
            a
            for a in assets
            if any(search(mt, a.name, flags=IGNORECASE) for mt in MACHINE_TYPE_GROUP)
        ]
        LOGGER.info(
            "Post machine type group %s, got %s: %s",
            MACHINE_TYPE_GROUP,
            counted_noun(assets, "asset"),
            [a.name for a in assets],
        )
    if not_endswith is not None:
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
    with TemporaryDirectory() as temp_dir:
        with get(
            asset.browser_download_url, headers=headers, timeout=timeout, stream=True
        ) as resp:
            resp.raise_for_status()
            dest = temp_dir / asset.name
            with dest.open(mode="wb") as fh:
                fh.writelines(resp.iter_content(chunk_size=chunk_size))
        LOGGER.info("Yielding %r...", str(dest))
        yield dest


##


def setup_asset(
    asset_owner: str,
    asset_repo: str,
    path: PathLike,
    /,
    *,
    token: Secret[str] | None = COMMON_SETTINGS.token,
    match_system: bool = COMMON_SETTINGS.match_system,
    match_machine: bool = COMMON_SETTINGS.match_machine,
    not_endswith: list[str] | None = COMMON_SETTINGS.not_endswith,
    timeout: int = COMMON_SETTINGS.timeout,
    chunk_size: int = COMMON_SETTINGS.chunk_size,
    sudo: bool = PERM_SETTINGS.sudo,
    perms: PermissionsLike | None = PERM_SETTINGS.perms,
    owner: str | int | None = PERM_SETTINGS.owner,
    group: str | int | None = PERM_SETTINGS.group,
) -> None:
    """Setup a GitHub asset."""
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - asset_owner   = %s
             - asset_repo    = %s
             - path          = %s
             - token         = %s
             - match_system  = %s
             - match_machine = %s
             - not_endswith  = %s
             - timeout       = %d
             - chunk_size    = %d
             - sudo          = %s
             - perms         = %s
             - owner         = %s
             - group         = %s
        """),
        setup_asset.__name__,
        __version__,
        asset_owner,
        asset_repo,
        path,
        token,
        match_system,
        match_machine,
        not_endswith,
        timeout,
        chunk_size,
        sudo,
        perms,
        owner,
        group,
    )
    with yield_asset(
        asset_owner,
        asset_repo,
        token=token,
        match_system=match_system,
        match_machine=match_machine,
        not_endswith=not_endswith,
        timeout=timeout,
        chunk_size=chunk_size,
    ) as src:
        cp(src, path, sudo=sudo, perms=perms, owner=owner, group=group)
        LOGGER.info("Downloaded to %r", str(path))


##


def setup_age(
    *,
    binary_name: str = AGE_SETTINGS.binary_name,
    token: Secret[str] | None = COMMON_SETTINGS.token,
    timeout: int = COMMON_SETTINGS.timeout,
    path_binaries: Path = PATH_BINARIES_SETTINGS.path_binaries,
    chunk_size: int = COMMON_SETTINGS.chunk_size,
    sudo: bool = PERM_SETTINGS.sudo,
    perms: PermissionsLike | None = PERM_SETTINGS.perms,
    owner: str | int | None = PERM_SETTINGS.owner,
    group: str | int | None = PERM_SETTINGS.group,
) -> None:
    """Setup 'age'."""
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - binary_name   = %s
             - token         = %s
             - timeout       = %s
             - path_binaries = %s
             - chunk_size    = %s
             - sudo          = %s
             - perms         = %s
             - owner         = %s
             - group         = %s
        """),
        setup_age.__name__,
        __version__,
        binary_name,
        token,
        timeout,
        path_binaries,
        chunk_size,
        sudo,
        perms,
        owner,
        group,
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
    token: Secret[str] | None = COMMON_SETTINGS.token,
    timeout: int = COMMON_SETTINGS.timeout,
    path_binaries: Path = PATH_BINARIES_SETTINGS.path_binaries,
    chunk_size: int = COMMON_SETTINGS.chunk_size,
    sudo: bool = PERM_SETTINGS.sudo,
    perms: PermissionsLike | None = PERM_SETTINGS.perms,
    owner: str | int | None = PERM_SETTINGS.owner,
    group: str | int | None = PERM_SETTINGS.group,
) -> None:
    """Setup 'sops'."""
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - binary_name   = %s
             - token         = %s
             - timeout       = %s
             - path_binaries = %s
             - chunk_size    = %s
             - sudo          = %s
             - perms         = %s
             - owner         = %s
             - group         = %s
        """),
        setup_sops.__name__,
        __version__,
        binary_name,
        token,
        timeout,
        path_binaries,
        chunk_size,
        sudo,
        perms,
        owner,
        group,
    )
    setup_asset(
        "getsops",
        "sops",
        Path(path_binaries / binary_name),
        token=token,
        match_system=True,
        match_machine=True,
        not_endswith=["json"],
        timeout=timeout,
        chunk_size=chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
    )


__all__ = ["setup_age", "setup_asset", "setup_sops", "yield_asset"]
