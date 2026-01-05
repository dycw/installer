from __future__ import annotations

from re import IGNORECASE, search
from typing import TYPE_CHECKING

from github.Auth import Token
from requests import get
from typed_settings import Secret
from utilities.iterables import one

from github_downloader.settings import SETTINGS

if TYPE_CHECKING:
    from pathlib import Path

    from actions.types import StrDict
    from typed_settings import Secret


def download_release(
    *,
    token: Secret[str] | None = SETTINGS.token,
    system: str = SETTINGS.system,
    machine: str = SETTINGS.machine,
    path_binary: Path = SETTINGS.path_binary,
    timeout: int = SETTINGS.timeout,
    chunk_size: int = SETTINGS.chunk_size,
) -> None:
    gh = GitHub(auth=None if token is None else Token(token.get_secret_value()))
    repo = gh.get_repo("getsops/sops")
    release = repo.get_latest_release()
    if system not in {"Darwin", "Linux"}:
        msg = f"Invalid system {system!r}"
        raise ValueError(msg)
    asset = one(
        a
        for a in release.get_assets()
        if search(system, a.name, flags=IGNORECASE)
        and search(machine, a.name, flags=IGNORECASE)
        and not a.name.endswith("json")
    )
    headers: StrDict = {}
    if token is not None:
        headers["Authorization"] = f"Bearer {token.get_secret_value()}"
    with get(
        asset.browser_download_url, headers=headers, timeout=timeout, stream=True
    ) as resp:
        resp.raise_for_status()
        path_binary.parent.mkdir(parents=True, exist_ok=True)
        with path_binary.open(mode="wb") as fh:
            fh.writelines(resp.iter_content(chunk_size=chunk_size))
    path_binary.chmod(0o755)
