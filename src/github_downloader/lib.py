from __future__ import annotations

from re import IGNORECASE, search
from typing import TYPE_CHECKING, Any

from github import Github
from github.Auth import Token
from requests import get
from typed_settings import Secret
from utilities.iterables import OneNonUniqueError, one
from utilities.subprocess import chmod

from github_downloader.constants import MACHINE_TYPE, SYSTEM_NAME
from github_downloader.logging import LOGGER
from github_downloader.settings import SETTINGS, SOPS_SETTINGS

if TYPE_CHECKING:
    from pathlib import Path

    from typed_settings import Secret


def download_release(
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
    gh = Github(auth=None if token is None else Token(token.get_secret_value()))
    repository = gh.get_repo(f"{owner}/{repo}")
    release = repository.get_latest_release()
    if SYSTEM_NAME not in {"Darwin", "Linux"}:
        msg = f"Invalid system {SYSTEM_NAME!r}"
        raise ValueError(msg)
    assets = list(release.get_assets())
    if match_system:
        assets = [a for a in assets if search(SYSTEM_NAME, a.name, flags=IGNORECASE)]
    if match_machine:
        assets = [a for a in assets if search(MACHINE_TYPE, a.name, flags=IGNORECASE)]
    assets = [a for a in assets if all(not a.name.endswith(e) for e in not_endswith)]
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


def download_sops(
    *,
    binary_name: str = SOPS_SETTINGS.binary_name,
    token: Secret[str] | None = SOPS_SETTINGS.token,
    timeout: int = SOPS_SETTINGS.timeout,
    path_binaries: Path = SOPS_SETTINGS.path_binaries,
    chunk_size: int = SOPS_SETTINGS.chunk_size,
    permissions: str = SOPS_SETTINGS.permissions,
) -> None:
    """Download 'sops'."""
    download_release(
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


__all__ = ["download_release"]
