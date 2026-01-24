from __future__ import annotations

from contextlib import contextmanager
from re import IGNORECASE, search
from typing import TYPE_CHECKING, Any

from github import Github
from github.Auth import Token
from requests import get
from utilities.core import (
    OneNonUniqueError,
    TemporaryDirectory,
    log_info,
    one,
    yield_bz2,
    yield_gzip,
    yield_lzma,
)
from utilities.inflect import counted_noun
from utilities.tabulate import func_param_desc

from installer import __version__
from installer.apps.constants import (
    C_STD_LIB_GROUP,
    GITHUB_TOKEN,
    MACHINE_TYPE_GROUP,
    SYSTEM_NAME_GROUP,
)

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

    from typed_settings import Secret
    from utilities.types import LoggerLike, MaybeSequenceStr


@contextmanager
def yield_asset(
    owner: str,
    repo: str,
    /,
    *,
    logger: LoggerLike | None = None,
    tag: str | None = None,
    token: Secret[str] | None = GITHUB_TOKEN,
    match_system: bool = False,
    match_c_std_lib: bool = False,
    match_machine: bool = False,
    not_matches: MaybeSequenceStr | None = None,
    not_endswith: MaybeSequenceStr | None = None,
) -> Iterator[Path]:
    """Yield a GitHub asset."""
    log_info(
        logger,
        func_param_desc(
            yield_asset,
            __version__,
            f"{owner=}",
            f"{repo=}",
            f"{logger=}",
            f"{tag=}",
            f"{token=}",
            f"{match_system=}",
            f"{match_c_std_lib=}",
            f"{match_machine=}",
            f"{not_matches=}",
            f"{not_endswith=}",
        ),
    )
    gh = Github(auth=None if token is None else Token(token.get_secret_value()))
    repository = gh.get_repo(f"{owner}/{repo}")
    if tag is None:
        release = repository.get_latest_release()
    else:
        release = next(r for r in repository.get_releases() if search(tag, r.tag_name))
    assets = list(release.get_assets())
    log_info(
        logger, "Got %s: %s", counted_noun(assets, "asset"), [a.name for a in assets]
    )
    if match_system:
        assets = [
            a
            for a in assets
            if any(search(c, a.name, flags=IGNORECASE) for c in SYSTEM_NAME_GROUP)
        ]
        log_info(
            logger,
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
        log_info(
            logger,
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
        log_info(
            logger,
            "Post machine type group %s, got %s: %s",
            MACHINE_TYPE_GROUP,
            counted_noun(assets, "asset"),
            [a.name for a in assets],
        )
    if not_matches is not None:
        assets = [
            a for a in assets if all(search(p, a.name) is None for p in not_matches)
        ]
        log_info(
            logger,
            "Post asset name patterns, got %s: %s",
            counted_noun(assets, "asset"),
            [a.name for a in assets],
        )
    if not_endswith is not None:
        assets = [
            a for a in assets if all(not a.name.endswith(e) for e in not_endswith)
        ]
        log_info(
            logger,
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
        log_info(logger, "Yielding %r...", str(dest))
        yield dest


##


@contextmanager
def yield_bz2_asset(
    owner: str,
    repo: str,
    /,
    *,
    tag: str | None = None,
    token: Secret[str] | None = GITHUB_TOKEN,
    match_system: bool = False,
    match_c_std_lib: bool = False,
    match_machine: bool = False,
    not_matches: MaybeSequenceStr | None = None,
    not_endswith: MaybeSequenceStr | None = None,
) -> Iterator[Path]:
    log_info(
        logger,
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
        ),
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
        yield_bz2(temp1) as temp2,
    ):
        yield temp2


##


@contextmanager
def yield_gzip_asset(
    owner: str,
    repo: str,
    /,
    *,
    tag: str | None = None,
    token: Secret[str] | None = GITHUB_TOKEN,
    match_system: bool = False,
    match_c_std_lib: bool = False,
    match_machine: bool = False,
    not_matches: MaybeSequenceStr | None = None,
    not_endswith: MaybeSequenceStr | None = None,
) -> Iterator[Path]:
    log_info(
        logger,
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
        ),
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
        yield_gzip(temp1) as temp2,
    ):
        yield temp2


##


@contextmanager
def yield_lzma_asset(
    owner: str,
    repo: str,
    /,
    *,
    tag: str | None = None,
    token: Secret[str] | None = GITHUB_TOKEN,
    match_system: bool = False,
    match_c_std_lib: bool = False,
    match_machine: bool = False,
    not_matches: MaybeSequenceStr | None = None,
    not_endswith: MaybeSequenceStr | None = None,
) -> Iterator[Path]:
    log_info(
        logger,
        func_param_desc(
            yield_lzma_asset,
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
        ),
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
        yield_lzma(temp1) as temp2,
    ):
        yield temp2


__all__ = ["yield_asset", "yield_bz2_asset", "yield_gzip_asset", "yield_lzma_asset"]
