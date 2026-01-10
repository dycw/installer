from __future__ import annotations

import bz2
import tarfile
from contextlib import contextmanager
from re import IGNORECASE, search
from shutil import copyfileobj
from typing import TYPE_CHECKING, Any

from github import Github
from github.Auth import Token
from requests import get
from utilities.inflect import counted_noun
from utilities.iterables import OneNonUniqueError, one
from utilities.tempfile import TemporaryDirectory, TemporaryFile

from github_downloader.constants import C_STD_LIB_GROUP, MACHINE_TYPE_GROUP, SYSTEM_NAME
from github_downloader.logging import LOGGER
from github_downloader.settings import DOWNLOAD_SETTINGS, MATCH_SETTINGS

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

    from typed_settings import Secret


@contextmanager
def yield_asset(
    owner: str,
    repo: str,
    /,
    *,
    token: Secret[str] | None = DOWNLOAD_SETTINGS.token,
    match_system: bool = MATCH_SETTINGS.match_system,
    match_c_std_lib: bool = MATCH_SETTINGS.match_c_std_lib,
    match_machine: bool = MATCH_SETTINGS.match_machine,
    not_matches: list[str] | None = MATCH_SETTINGS.not_matches,
    not_endswith: list[str] | None = MATCH_SETTINGS.not_endswith,
    timeout: int = DOWNLOAD_SETTINGS.timeout,
    chunk_size: int = DOWNLOAD_SETTINGS.chunk_size,
) -> Iterator[Path]:
    """Yield a GitHub asset."""
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
    if match_c_std_lib and (C_STD_LIB_GROUP is not None):
        assets = [
            a
            for a in assets
            if any(search(c, a.name, flags=IGNORECASE) for c in C_STD_LIB_GROUP)
        ]
        LOGGER.info(
            "Post C std. lib. group %s, got %s: %s",
            C_STD_LIB_GROUP,
            counted_noun(assets, "asset"),
            [a.name for a in assets],
        )
    if match_machine:
        assets = [
            a
            for a in assets
            if any(search(m, a.name, flags=IGNORECASE) for m in MACHINE_TYPE_GROUP)
        ]
        LOGGER.info(
            "Post machine type group %s, got %s: %s",
            MACHINE_TYPE_GROUP,
            counted_noun(assets, "asset"),
            [a.name for a in assets],
        )
    if not_matches is not None:
        assets = [
            a for a in assets if all(search(p, a.name) is None for p in not_matches)
        ]
        LOGGER.info(
            "Post asset name patterns, got %s: %s",
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


@contextmanager
def yield_bz2_asset(
    owner: str,
    repo: str,
    /,
    *,
    token: Secret[str] | None = DOWNLOAD_SETTINGS.token,
    match_system: bool = MATCH_SETTINGS.match_system,
    match_c_std_lib: bool = MATCH_SETTINGS.match_c_std_lib,
    match_machine: bool = MATCH_SETTINGS.match_machine,
    not_matches: list[str] | None = MATCH_SETTINGS.not_matches,
    not_endswith: list[str] | None = MATCH_SETTINGS.not_endswith,
    timeout: int = DOWNLOAD_SETTINGS.timeout,
    chunk_size: int = DOWNLOAD_SETTINGS.chunk_size,
) -> Iterator[Path]:
    with (
        yield_asset(
            owner,
            repo,
            token=token,
            match_system=match_system,
            match_c_std_lib=match_c_std_lib,
            match_machine=match_machine,
            not_matches=not_matches,
            not_endswith=not_endswith,
            timeout=timeout,
            chunk_size=chunk_size,
        ) as temp1,
        bz2.open(temp1) as bz,
        TemporaryFile() as temp2,
        temp2.open(mode="wb") as fh,
    ):
        copyfileobj(bz, fh)
        yield temp2


##


@contextmanager
def yield_tar_asset(
    owner: str,
    repo: str,
    /,
    *,
    token: Secret[str] | None = DOWNLOAD_SETTINGS.token,
    match_system: bool = MATCH_SETTINGS.match_system,
    match_c_std_lib: bool = MATCH_SETTINGS.match_c_std_lib,
    match_machine: bool = MATCH_SETTINGS.match_machine,
    not_matches: list[str] | None = MATCH_SETTINGS.not_matches,
    not_endswith: list[str] | None = MATCH_SETTINGS.not_endswith,
    timeout: int = DOWNLOAD_SETTINGS.timeout,
    chunk_size: int = DOWNLOAD_SETTINGS.chunk_size,
) -> Iterator[Path]:
    with (
        yield_asset(
            owner,
            repo,
            token=token,
            match_system=match_system,
            match_c_std_lib=match_c_std_lib,
            match_machine=match_machine,
            not_matches=not_matches,
            not_endswith=not_endswith,
            timeout=timeout,
            chunk_size=chunk_size,
        ) as temp1,
        tarfile.open(name=temp1, mode="r:gz") as tar,
        TemporaryDirectory() as temp2,
    ):
        tar.extractall(temp2, filter="data")
        try:
            yield one(temp2.iterdir())
        except OneNonUniqueError:
            yield temp2


__all__ = ["yield_asset", "yield_bz2_asset", "yield_tar_asset"]
