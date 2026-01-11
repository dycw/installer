from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, assert_never

from typed_settings import Secret
from utilities.subprocess import APT_UPDATE, apt_install_cmd, cp, maybe_sudo_cmd, run
from utilities.text import repr_str, strip_and_dedent

from github_downloader import __version__
from github_downloader.constants import SHELL, SYSTEM_NAME
from github_downloader.download import yield_asset, yield_bz2_asset, yield_tar_asset
from github_downloader.logging import LOGGER
from github_downloader.settings import (
    DOWNLOAD_SETTINGS,
    ETC_SETTINGS,
    MATCH_SETTINGS,
    PATH_BINARIES_SETTINGS,
    PERMS_SETTINGS,
    SUDO_SETTINGS,
)
from github_downloader.utilities import ensure_shell_rc

if TYPE_CHECKING:
    from typed_settings import Secret
    from utilities.permissions import PermissionsLike
    from utilities.types import PathLike


def setup_asset(
    asset_owner: str,
    asset_repo: str,
    path: PathLike,
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
    sudo: bool = SUDO_SETTINGS.sudo,
    perms: PermissionsLike | None = PERMS_SETTINGS.perms,
    owner: str | int | None = PERMS_SETTINGS.owner,
    group: str | int | None = PERMS_SETTINGS.group,
) -> None:
    """Setup a GitHub asset."""
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - asset_owner     = %s
             - asset_repo      = %s
             - path            = %s
             - token           = %s
             - match_system    = %s
             - match_c_std_lib = %s
             - match_machine   = %s
             - not_matches    = %s
             - not_endswith    = %s
             - timeout         = %d
             - chunk_size      = %d
             - sudo            = %s
             - perms           = %s
             - owner           = %s
             - group           = %s
        """),
        setup_asset.__name__,
        __version__,
        asset_owner,
        asset_repo,
        path,
        token,
        match_system,
        match_c_std_lib,
        match_machine,
        not_matches,
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
        match_c_std_lib=match_c_std_lib,
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
    token: Secret[str] | None = DOWNLOAD_SETTINGS.token,
    timeout: int = DOWNLOAD_SETTINGS.timeout,
    path_binaries: PathLike = PATH_BINARIES_SETTINGS.path_binaries,
    chunk_size: int = DOWNLOAD_SETTINGS.chunk_size,
    sudo: bool = SUDO_SETTINGS.sudo,
    perms: PermissionsLike | None = PERMS_SETTINGS.perms,
    owner: str | int | None = PERMS_SETTINGS.owner,
    group: str | int | None = PERMS_SETTINGS.group,
) -> None:
    """Setup 'age'."""
    with yield_tar_asset(
        "FiloSottile",
        "age",
        token=token,
        match_system=True,
        match_machine=True,
        not_endswith=["proof"],
        timeout=timeout,
        chunk_size=chunk_size,
    ) as temp:
        downloads: list[Path] = []
        for src in temp.iterdir():
            if src.name.startswith("age"):
                dest = Path(path_binaries, src.name)
                cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
                downloads.append(dest)
        LOGGER.info("Downloaded to %s", ", ".join(map(repr_str, downloads)))


##


def setup_bottom(
    *,
    token: Secret[str] | None = DOWNLOAD_SETTINGS.token,
    timeout: int = DOWNLOAD_SETTINGS.timeout,
    path_binaries: PathLike = PATH_BINARIES_SETTINGS.path_binaries,
    chunk_size: int = DOWNLOAD_SETTINGS.chunk_size,
    sudo: bool = SUDO_SETTINGS.sudo,
    perms: PermissionsLike | None = PERMS_SETTINGS.perms,
    owner: str | int | None = PERMS_SETTINGS.owner,
    group: str | int | None = PERMS_SETTINGS.group,
) -> None:
    """Setup 'bottom'."""
    with yield_tar_asset(
        "ClementTsang",
        "bottom",
        token=token,
        match_system=True,
        match_c_std_lib=True,
        match_machine=True,
        not_matches=[r"\d+\.tar\.gz$"],
        timeout=timeout,
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "btm"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    LOGGER.info("Downloaded to %r", str(dest))


##


def setup_direnv(
    *,
    token: Secret[str] | None = DOWNLOAD_SETTINGS.token,
    timeout: int = DOWNLOAD_SETTINGS.timeout,
    path_binaries: PathLike = PATH_BINARIES_SETTINGS.path_binaries,
    chunk_size: int = DOWNLOAD_SETTINGS.chunk_size,
    sudo: bool = SUDO_SETTINGS.sudo,
    perms: PermissionsLike | None = PERMS_SETTINGS.perms,
    owner: str | int | None = PERMS_SETTINGS.owner,
    group: str | int | None = PERMS_SETTINGS.group,
    etc: bool = ETC_SETTINGS.etc,
) -> None:
    """Setup 'direnv'."""
    dest = Path(path_binaries, "direnv")
    setup_asset(
        "direnv",
        "direnv",
        dest,
        token=token,
        match_system=True,
        match_machine=True,
        timeout=timeout,
        chunk_size=chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
    )
    LOGGER.info("Downloaded to %r", str(dest))
    match SHELL:
        case "bash" | "zsh":
            line = f'eval "$(direnv hook {SHELL})"'
        case "fish":
            line = "direnv hook fish | source"
        case never:
            assert_never(never)
    ensure_shell_rc(line, etc="direnv" if etc else None)


##


def setup_fzf(
    *,
    token: Secret[str] | None = DOWNLOAD_SETTINGS.token,
    timeout: int = DOWNLOAD_SETTINGS.timeout,
    path_binaries: PathLike = PATH_BINARIES_SETTINGS.path_binaries,
    chunk_size: int = DOWNLOAD_SETTINGS.chunk_size,
    sudo: bool = SUDO_SETTINGS.sudo,
    perms: PermissionsLike | None = PERMS_SETTINGS.perms,
    owner: str | int | None = PERMS_SETTINGS.owner,
    group: str | int | None = PERMS_SETTINGS.group,
    etc: bool = ETC_SETTINGS.etc,
) -> None:
    """Setup 'fzf'."""
    with yield_tar_asset(
        "junegunn",
        "fzf",
        token=token,
        match_system=True,
        match_machine=True,
        timeout=timeout,
        chunk_size=chunk_size,
    ) as src:
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    LOGGER.info("Downloaded to %r", str(dest))
    match SHELL:
        case "bash":
            line = 'eval "$(fzf --bash)"'
        case "zsh":
            line = "source <(fzf --zsh)"
        case "fish":
            line = "fzf --fish | source"
        case never:
            assert_never(never)
    ensure_shell_rc(line, etc="fzf" if etc else None)


##


def setup_git(*, sudo: bool = SUDO_SETTINGS.sudo) -> None:
    """Setup 'git'."""
    match SYSTEM_NAME:
        case "Darwin":
            msg = f"Unsupported system: {SYSTEM_NAME!r}"
            raise ValueError(msg)
        case "Linux":
            run(*maybe_sudo_cmd(*APT_UPDATE, sudo=sudo))
            run(*maybe_sudo_cmd(*apt_install_cmd("git"), sudo=sudo))
            LOGGER.info("Installed 'git'")
        case never:
            assert_never(never)


##


def setup_just(
    *,
    token: Secret[str] | None = DOWNLOAD_SETTINGS.token,
    timeout: int = DOWNLOAD_SETTINGS.timeout,
    path_binaries: PathLike = PATH_BINARIES_SETTINGS.path_binaries,
    chunk_size: int = DOWNLOAD_SETTINGS.chunk_size,
    sudo: bool = SUDO_SETTINGS.sudo,
    perms: PermissionsLike | None = PERMS_SETTINGS.perms,
    owner: str | int | None = PERMS_SETTINGS.owner,
    group: str | int | None = PERMS_SETTINGS.group,
) -> None:
    """Setup 'just'."""
    with yield_tar_asset(
        "casey",
        "just",
        token=token,
        match_system=True,
        match_machine=True,
        timeout=timeout,
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "just"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    LOGGER.info("Downloaded to %r", str(dest))


##


def setup_restic(
    *,
    token: Secret[str] | None = DOWNLOAD_SETTINGS.token,
    timeout: int = DOWNLOAD_SETTINGS.timeout,
    path_binaries: PathLike = PATH_BINARIES_SETTINGS.path_binaries,
    chunk_size: int = DOWNLOAD_SETTINGS.chunk_size,
    sudo: bool = SUDO_SETTINGS.sudo,
    perms: PermissionsLike | None = PERMS_SETTINGS.perms,
    owner: str | int | None = PERMS_SETTINGS.owner,
    group: str | int | None = PERMS_SETTINGS.group,
) -> None:
    """Setup 'restic'."""
    with yield_bz2_asset(
        "restic",
        "restic",
        token=token,
        match_system=True,
        match_machine=True,
        timeout=timeout,
        chunk_size=chunk_size,
    ) as src:
        dest = Path(path_binaries, "restic")
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    LOGGER.info("Downloaded to %r", str(dest))


##


def setup_ripgrep(
    *,
    token: Secret[str] | None = DOWNLOAD_SETTINGS.token,
    timeout: int = DOWNLOAD_SETTINGS.timeout,
    path_binaries: PathLike = PATH_BINARIES_SETTINGS.path_binaries,
    chunk_size: int = DOWNLOAD_SETTINGS.chunk_size,
    sudo: bool = SUDO_SETTINGS.sudo,
    perms: PermissionsLike | None = PERMS_SETTINGS.perms,
    owner: str | int | None = PERMS_SETTINGS.owner,
    group: str | int | None = PERMS_SETTINGS.group,
) -> None:
    """Setup 'ripgrep'."""
    with yield_tar_asset(
        "burntsushi",
        "ripgrep",
        token=token,
        match_system=True,
        match_machine=True,
        not_endswith=["sha256"],
        timeout=timeout,
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "rg"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    LOGGER.info("Downloaded to %r", str(dest))


##


def setup_starship(
    *,
    token: Secret[str] | None = DOWNLOAD_SETTINGS.token,
    timeout: int = DOWNLOAD_SETTINGS.timeout,
    path_binaries: PathLike = PATH_BINARIES_SETTINGS.path_binaries,
    chunk_size: int = DOWNLOAD_SETTINGS.chunk_size,
    sudo: bool = SUDO_SETTINGS.sudo,
    perms: PermissionsLike | None = PERMS_SETTINGS.perms,
    owner: str | int | None = PERMS_SETTINGS.owner,
    group: str | int | None = PERMS_SETTINGS.group,
    etc: bool = ETC_SETTINGS.etc,
) -> None:
    """Setup 'starship'."""
    with yield_tar_asset(
        "starship",
        "starship",
        token=token,
        match_system=True,
        match_c_std_lib=True,
        match_machine=True,
        not_endswith=["sha256"],
        timeout=timeout,
        chunk_size=chunk_size,
    ) as src:
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    LOGGER.info("Downloaded to %r", str(dest))
    match SHELL:
        case "bash" | "zsh":
            line = f'eval "$(starship init {SHELL})"'
        case "fish":
            line = "starship init fish | source"
        case never:
            assert_never(never)
    ensure_shell_rc(line, etc="starship" if etc else None)


##


def setup_sops(
    *,
    token: Secret[str] | None = DOWNLOAD_SETTINGS.token,
    timeout: int = DOWNLOAD_SETTINGS.timeout,
    path_binaries: PathLike = PATH_BINARIES_SETTINGS.path_binaries,
    chunk_size: int = DOWNLOAD_SETTINGS.chunk_size,
    sudo: bool = SUDO_SETTINGS.sudo,
    perms: PermissionsLike | None = PERMS_SETTINGS.perms,
    owner: str | int | None = PERMS_SETTINGS.owner,
    group: str | int | None = PERMS_SETTINGS.group,
) -> None:
    """Setup 'sops'."""
    dest = Path(path_binaries, "sops")
    setup_asset(
        "getsops",
        "sops",
        dest,
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
    LOGGER.info("Downloaded to %r", str(dest))


__all__ = [
    "setup_age",
    "setup_asset",
    "setup_direnv",
    "setup_fzf",
    "setup_git",
    "setup_just",
    "setup_restic",
    "setup_ripgrep",
    "setup_sops",
    "setup_starship",
]
