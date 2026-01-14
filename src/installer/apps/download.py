from __future__ import annotations

from contextlib import contextmanager
from re import IGNORECASE, search
from typing import TYPE_CHECKING, Any

from github import Github
from github.Auth import Token
from requests import get
from utilities.bz2 import yield_bz2_contents
from utilities.gzip import yield_gzip_contents
from utilities.inflect import counted_noun
from utilities.iterables import OneNonUniqueError, one
from utilities.tabulate import func_param_desc
from utilities.tempfile import TemporaryDirectory

from installer import __version__
from installer.apps.constants import (
    C_STD_LIB_GROUP,
    MACHINE_TYPE_GROUP,
    SYSTEM_NAME_GROUP,
)
from installer.apps.settings import DOWNLOAD_SETTINGS, MATCH_SETTINGS, TAG_SETTINGS
from installer.logging import LOGGER

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
    tag: str | None = TAG_SETTINGS.tag,
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
    LOGGER.info(
        func_param_desc(
            yield_asset,
            __version__,
            f"{owner=}",
            f"{repo=}",
            f"{tag=}",
            f"{token=}",
            f"{match_system=}",
            f"{match_c_std_lib=}",
            f"{match_machine=}",
            f"{not_matches=}",
            f"{not_endswith=}",
            f"{timeout=}",
            f"{chunk_size=}",
        )
    )
    gh = Github(auth=None if token is None else Token(token.get_secret_value()))
    repository = gh.get_repo(f"{owner}/{repo}")
    if tag is None:
        release = repository.get_latest_release()
    else:
        release = next(r for r in repository.get_releases() if search(tag, r.tag_name))
    assets = list(release.get_assets())
    LOGGER.info("Got %s: %s", counted_noun(assets, "asset"), [a.name for a in assets])
    if match_system:
        assets = [
            a
            for a in assets
            if any(search(c, a.name, flags=IGNORECASE) for c in SYSTEM_NAME_GROUP)
        ]
        LOGGER.info(
            "Post system name group %s, got %s: %s",
            SYSTEM_NAME_GROUP,
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
            "Post C standard library group %s, got %s: %s",
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
    tag: str | None = TAG_SETTINGS.tag,
    token: Secret[str] | None = DOWNLOAD_SETTINGS.token,
    match_system: bool = MATCH_SETTINGS.match_system,
    match_c_std_lib: bool = MATCH_SETTINGS.match_c_std_lib,
    match_machine: bool = MATCH_SETTINGS.match_machine,
    not_matches: list[str] | None = MATCH_SETTINGS.not_matches,
    not_endswith: list[str] | None = MATCH_SETTINGS.not_endswith,
    timeout: int = DOWNLOAD_SETTINGS.timeout,
    chunk_size: int = DOWNLOAD_SETTINGS.chunk_size,
) -> Iterator[Path]:
    LOGGER.info(
        func_param_desc(
            yield_bz2_asset,
            __version__,
            f"{owner=}",
            f"{repo=}",
            f"{tag=}",
            f"{token=}",
            f"{match_system=}",
            f"{match_c_std_lib=}",
            f"{match_machine=}",
            f"{not_matches=}",
            f"{not_endswith=}",
            f"{timeout=}",
            f"{chunk_size=}",
        )
    )
    with (
        yield_asset(
            owner,
            repo,
            tag=tag,
            token=token,
            match_system=match_system,
            match_c_std_lib=match_c_std_lib,
            match_machine=match_machine,
            not_matches=not_matches,
            not_endswith=not_endswith,
            timeout=timeout,
            chunk_size=chunk_size,
        ) as temp1,
        yield_bz2_contents(temp1) as temp2,
    ):
        yield temp2


##


@contextmanager
def yield_gzip_asset(
    owner: str,
    repo: str,
    /,
    *,
    tag: str | None = TAG_SETTINGS.tag,
    token: Secret[str] | None = DOWNLOAD_SETTINGS.token,
    match_system: bool = MATCH_SETTINGS.match_system,
    match_c_std_lib: bool = MATCH_SETTINGS.match_c_std_lib,
    match_machine: bool = MATCH_SETTINGS.match_machine,
    not_matches: list[str] | None = MATCH_SETTINGS.not_matches,
    not_endswith: list[str] | None = MATCH_SETTINGS.not_endswith,
    timeout: int = DOWNLOAD_SETTINGS.timeout,
    chunk_size: int = DOWNLOAD_SETTINGS.chunk_size,
) -> Iterator[Path]:
    LOGGER.info(
        func_param_desc(
            yield_gzip_asset,
            __version__,
            f"{owner=}",
            f"{repo=}",
            f"{tag=}",
            f"{token=}",
            f"{match_system=}",
            f"{match_c_std_lib=}",
            f"{match_machine=}",
            f"{not_matches=}",
            f"{not_endswith=}",
            f"{timeout=}",
            f"{chunk_size=}",
        )
    )
    with (
        yield_asset(
            owner,
            repo,
            tag=tag,
            token=token,
            match_system=match_system,
            match_c_std_lib=match_c_std_lib,
            match_machine=match_machine,
            not_matches=not_matches,
            not_endswith=not_endswith,
            timeout=timeout,
            chunk_size=chunk_size,
        ) as temp1,
        yield_gzip_contents(temp1) as temp2,
    ):
        yield temp2


__all__ = ["yield_asset", "yield_bz2_asset", "yield_gzip_asset", "yield_gzip_asset"]
