from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, assert_never

from typed_settings import Secret
from utilities.subprocess import (
    APT_UPDATE,
    apt_install_cmd,
    cp,
    maybe_sudo_cmd,
    run,
    symlink,
)
from utilities.tabulate import func_param_desc
from utilities.text import repr_str

from installer import __version__
from installer.apps.constants import SHELL, SYSTEM_NAME
from installer.apps.download import (
    yield_asset,
    yield_bz2_asset,
    yield_gzip_asset,
    yield_lzma_asset,
)
from installer.apps.settings import (
    DOWNLOAD_SETTINGS,
    MATCH_SETTINGS,
    PATH_BINARIES_SETTINGS,
    PERMS_SETTINGS,
    SHELL_RC_SETTINGS,
    TAG_SETTINGS,
)
from installer.logging import LOGGER
from installer.settings import SUDO_SETTINGS
from installer.utilities import ensure_shell_rc

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
    tag: str | None = TAG_SETTINGS.tag,
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
        func_param_desc(
            setup_asset,
            __version__,
            f"{asset_owner=}",
            f"{asset_repo=}",
            f"{path=}",
            f"{tag=}",
            f"{token=}",
            f"{match_system=}",
            f"{match_c_std_lib=}",
            f"{match_machine=}",
            f"{not_matches=}",
            f"{not_endswith=}",
            f"{timeout=}",
            f"{chunk_size=}",
            f"{sudo=}",
            f"{perms=}",
            f"{owner=}",
            f"{group=}",
        )
    )
    with yield_asset(
        asset_owner,
        asset_repo,
        tag=tag,
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
    with yield_gzip_asset(
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


def setup_bat(
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
    """Setup 'bat'."""
    with yield_gzip_asset(
        "sharkdp",
        "bat",
        token=token,
        match_system=True,
        match_c_std_lib=True,
        match_machine=True,
        timeout=timeout,
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "bat"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    LOGGER.info("Downloaded to %r", str(dest))


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
    with yield_gzip_asset(
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


def setup_curl(*, sudo: bool = SUDO_SETTINGS.sudo) -> None:
    """Setup 'curl'."""
    match SYSTEM_NAME:
        case "Darwin":
            msg = f"Unsupported system: {SYSTEM_NAME!r}"
            raise ValueError(msg)
        case "Linux":
            run(*maybe_sudo_cmd(*APT_UPDATE, sudo=sudo))
            run(*maybe_sudo_cmd(*apt_install_cmd("curl"), sudo=sudo))
            LOGGER.info("Installed 'curl'")
        case never:
            assert_never(never)


##


def setup_delta(
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
    """Setup 'delta'."""
    with yield_gzip_asset(
        "dandavison",
        "delta",
        token=token,
        match_system=True,
        match_c_std_lib=True,
        match_machine=True,
        timeout=timeout,
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "delta"
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
    skip_shell_rc: bool = SHELL_RC_SETTINGS.skip_shell_rc,
    etc: bool = SHELL_RC_SETTINGS.etc,
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
    if not skip_shell_rc:
        match SHELL:
            case "bash" | "zsh":
                line = f'eval "$(direnv hook {SHELL})"'
            case "fish":
                line = "direnv hook fish | source"
            case "posix":
                msg = f"Unsupported shell: {SHELL=}"
                raise TypeError(msg)
            case never:
                assert_never(never)
        ensure_shell_rc(line, etc="direnv" if etc else None)


##


def setup_dust(
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
    """Setup 'dust'."""
    match SYSTEM_NAME:
        case "Darwin":
            match_machine = False
        case "Linux":
            match_machine = True
        case never:
            assert_never(never)
    with yield_gzip_asset(
        "bootandy",
        "dust",
        token=token,
        match_system=True,
        match_c_std_lib=True,
        match_machine=match_machine,
        timeout=timeout,
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "dust"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    LOGGER.info("Downloaded to %r", str(dest))


##


def setup_eza(
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
    """Setup 'eza'."""
    match SYSTEM_NAME:
        case "Darwin":
            asset_owner = "cargo-bins"
            asset_repo = "cargo-quickinstall"
            tag = "eza"
            match_c_std_lib = False
            not_endswith = ["sig"]
        case "Linux":
            asset_owner = "eza-community"
            asset_repo = "eza"
            tag = None
            match_c_std_lib = True
            not_endswith = ["zip"]
        case never:
            assert_never(never)
    with yield_gzip_asset(
        asset_owner,
        asset_repo,
        tag=tag,
        token=token,
        match_system=True,
        match_c_std_lib=match_c_std_lib,
        match_machine=True,
        not_endswith=not_endswith,
        timeout=timeout,
        chunk_size=chunk_size,
    ) as src:
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    LOGGER.info("Downloaded to %r", str(dest))


##


def setup_fd(
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
    """Setup 'fd'."""
    with yield_gzip_asset(
        "sharkdp",
        "fd",
        token=token,
        match_system=True,
        match_c_std_lib=True,
        match_machine=True,
        timeout=timeout,
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "fd"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    LOGGER.info("Downloaded to %r", str(dest))


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
    skip_shell_rc: bool = SHELL_RC_SETTINGS.skip_shell_rc,
    etc: bool = SHELL_RC_SETTINGS.etc,
) -> None:
    """Setup 'fzf'."""
    with yield_gzip_asset(
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
    if not skip_shell_rc:
        match SHELL:
            case "bash":
                line = 'eval "$(fzf --bash)"'
            case "zsh":
                line = "source <(fzf --zsh)"
            case "fish":
                line = "fzf --fish | source"
            case "posix":
                msg = f"Unsupported shell: {SHELL=}"
                raise TypeError(msg)
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


def setup_jq(
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
    """Setup 'shfmt'."""
    dest = Path(path_binaries, "jq")
    setup_asset(
        "jqlang",
        "jq",
        dest,
        token=token,
        match_system=True,
        match_machine=True,
        not_endswith=["linux64"],
        timeout=timeout,
        chunk_size=chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
    )
    LOGGER.info("Downloaded to %r", str(dest))


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
    with yield_gzip_asset(
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


def setup_neovim(
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
    """Setup 'neovim'."""
    with yield_gzip_asset(
        "neovim",
        "neovim",
        token=token,
        match_system=True,
        match_machine=True,
        not_endswith=["appimage", "zsync"],
        timeout=timeout,
        chunk_size=chunk_size,
    ) as temp:
        dest_dir = Path(path_binaries, "nvim-dir")
        cp(temp, dest_dir, sudo=sudo, perms=perms, owner=owner, group=group)
        dest_bin = Path(path_binaries, "nvim")
        symlink(dest_dir / "bin/nvim", dest_bin, sudo=sudo)
    LOGGER.info("Downloaded to %r", str(dest_bin))


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
    with yield_gzip_asset(
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
    skip_shell_rc: bool = SHELL_RC_SETTINGS.skip_shell_rc,
    etc: bool = SHELL_RC_SETTINGS.etc,
) -> None:
    """Setup 'starship'."""
    with yield_gzip_asset(
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
    if not skip_shell_rc:
        match SHELL:
            case "bash" | "zsh":
                line = f'eval "$(starship init {SHELL})"'
            case "fish":
                line = "starship init fish | source"
            case "posix":
                msg = f"Unsupported shell: {SHELL=}"
                raise TypeError(msg)
            case never:
                assert_never(never)
        ensure_shell_rc(line, etc="starship" if etc else None)


##


def setup_taplo(
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
    """Setup 'taplo'."""
    with yield_gzip_asset(
        "tamasfe",
        "taplo",
        token=token,
        match_system=True,
        match_machine=True,
        timeout=timeout,
        chunk_size=chunk_size,
    ) as src:
        dest = Path(path_binaries, "taplo")
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    LOGGER.info("Downloaded to %r", str(dest))


##


def setup_rsync(*, sudo: bool = SUDO_SETTINGS.sudo) -> None:
    """Setup 'rsync'."""
    match SYSTEM_NAME:
        case "Darwin":
            msg = f"Unsupported system: {SYSTEM_NAME!r}"
            raise ValueError(msg)
        case "Linux":
            run(*maybe_sudo_cmd(*APT_UPDATE, sudo=sudo))
            run(*maybe_sudo_cmd(*apt_install_cmd("rsync"), sudo=sudo))
            LOGGER.info("Installed 'rsync'")
        case never:
            assert_never(never)


##


def setup_ruff(
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
    """Setup 'ruff'."""
    with yield_gzip_asset(
        "astral-sh",
        "ruff",
        token=token,
        match_system=True,
        match_c_std_lib=True,
        match_machine=True,
        not_endswith=["sha256"],
        timeout=timeout,
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "ruff"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    LOGGER.info("Downloaded to %r", str(dest))


##


def setup_sd(
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
    """Setup 'sd'."""
    with yield_gzip_asset(
        "chmln",
        "sd",
        token=token,
        match_system=True,
        match_c_std_lib=True,
        match_machine=True,
        timeout=timeout,
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "sd"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    LOGGER.info("Downloaded to %r", str(dest))


##


def setup_shellcheck(
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
    """Setup 'shellcheck'."""
    with yield_gzip_asset(
        "koalaman",
        "shellcheck",
        token=token,
        match_system=True,
        match_machine=True,
        not_endswith=["tar.xz"],
        timeout=timeout,
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "shellcheck"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    LOGGER.info("Downloaded to %r", str(dest))


##


def setup_shfmt(
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
    """Setup 'shfmt'."""
    dest = Path(path_binaries, "shfmt")
    setup_asset(
        "mvdan",
        "sh",
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


##


def setup_uv(
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
    """Setup 'uv'."""
    with yield_gzip_asset(
        "astral-sh",
        "uv",
        token=token,
        match_system=True,
        match_c_std_lib=True,
        match_machine=True,
        not_endswith=["sha256"],
        timeout=timeout,
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "uv"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    LOGGER.info("Downloaded to %r", str(dest))


##


def setup_watchexec(
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
    """Setup 'watchexec'."""
    with yield_lzma_asset(
        "watchexec",
        "watchexec",
        token=token,
        match_system=True,
        match_c_std_lib=True,
        match_machine=True,
        not_endswith=["b3", "deb", "rpm", "sha256", "sha512"],
        timeout=timeout,
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "watchexec"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    LOGGER.info("Downloaded to %r", str(dest))


##


def setup_yq(
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
    """Setup 'yq'."""
    dest = Path(path_binaries, "yq")
    setup_asset(
        "mikefarah",
        "yq",
        dest,
        token=token,
        match_system=True,
        match_machine=True,
        not_endswith=["tar.gz"],
        timeout=timeout,
        chunk_size=chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
    )
    LOGGER.info("Downloaded to %r", str(dest))


##


def setup_zoxide(
    *,
    token: Secret[str] | None = DOWNLOAD_SETTINGS.token,
    timeout: int = DOWNLOAD_SETTINGS.timeout,
    path_binaries: PathLike = PATH_BINARIES_SETTINGS.path_binaries,
    chunk_size: int = DOWNLOAD_SETTINGS.chunk_size,
    sudo: bool = SUDO_SETTINGS.sudo,
    perms: PermissionsLike | None = PERMS_SETTINGS.perms,
    owner: str | int | None = PERMS_SETTINGS.owner,
    group: str | int | None = PERMS_SETTINGS.group,
    skip_shell_rc: bool = SHELL_RC_SETTINGS.skip_shell_rc,
    etc: bool = SHELL_RC_SETTINGS.etc,
) -> None:
    """Setup 'zoxide'."""
    with yield_gzip_asset(
        "ajeetdsouza",
        "zoxide",
        token=token,
        match_system=True,
        match_machine=True,
        timeout=timeout,
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "zoxide"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    LOGGER.info("Downloaded to %r", str(dest))
    if not skip_shell_rc:
        match SHELL:
            case "bash" | "zsh":
                line = f'eval "$(fzf --{SHELL})"'
            case "fish":
                line = "zoxide init fish | source"
            case "posix":
                msg = f"Unsupported shell: {SHELL=}"
                raise TypeError(msg)
            case never:
                assert_never(never)
        ensure_shell_rc(line, etc="zoxide" if etc else None)


__all__ = [
    "setup_age",
    "setup_asset",
    "setup_bat",
    "setup_bottom",
    "setup_curl",
    "setup_delta",
    "setup_direnv",
    "setup_dust",
    "setup_eza",
    "setup_fd",
    "setup_fzf",
    "setup_git",
    "setup_jq",
    "setup_just",
    "setup_neovim",
    "setup_restic",
    "setup_ripgrep",
    "setup_rsync",
    "setup_ruff",
    "setup_sd",
    "setup_shellcheck",
    "setup_shfmt",
    "setup_sops",
    "setup_starship",
    "setup_taplo",
    "setup_uv",
    "setup_yq",
    "setup_zoxide",
]
