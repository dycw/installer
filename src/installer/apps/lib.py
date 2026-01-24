from __future__ import annotations

import re
from pathlib import Path
from shlex import join
from typing import TYPE_CHECKING, assert_never

import utilities.subprocess
from typed_settings import Secret
from utilities.core import (
    WhichError,
    extract_group,
    log_info,
    normalize_multi_line_str,
    one,
    repr_str,
    which,
)
from utilities.logging import to_logger
from utilities.subprocess import (
    APT_UPDATE,
    BASH_LS,
    apt_install,
    apt_install_cmd,
    apt_remove,
    apt_update,
    chmod,
    cp,
    curl,
    curl_cmd,
    install,
    maybe_sudo_cmd,
    run,
    symlink,
    tee,
    yield_ssh_temp_dir,
)
from utilities.tabulate import func_param_desc

from installer import __version__
from installer.apps.constants import GITHUB_TOKEN, PATH_BINARIES, SHELL, SYSTEM_NAME
from installer.apps.download import (
    yield_asset,
    yield_bz2_asset,
    yield_gzip_asset,
    yield_lzma_asset,
)
from installer.configs.lib import setup_shell_config
from installer.configs.settings import FILE_SYSTEM_ROOT
from installer.utilities import split_ssh, ssh_install

if TYPE_CHECKING:
    from typed_settings import Secret
    from utilities.core import PermissionsLike
    from utilities.types import LoggerLike, MaybeSequenceStr, PathLike, Retry


def setup_apt_package(
    package: str,
    /,
    *,
    logger: LoggerLike | None = None,
    ssh: str | None = None,
    sudo: bool = False,
    retry: Retry | None = None,
) -> None:
    """Setup an 'apt' package."""
    log_info(
        logger,
        "%s",
        func_param_desc(
            setup_apt_package,
            __version__,
            f"{logger=}",
            f"{ssh=}",
            f"{sudo=}",
            f"{retry=}",
        ),
    )
    if ssh is None:
        match SYSTEM_NAME:
            case "Darwin":
                msg = f"Unsupported system: {SYSTEM_NAME!r}"
                raise ValueError(msg)
            case "Linux":
                run(*maybe_sudo_cmd(*APT_UPDATE, sudo=sudo))
                run(*maybe_sudo_cmd(*apt_install_cmd(package), sudo=sudo))
                log_info(logger, "Installed %r", package)
            case never:
                assert_never(never)
    else:
        ssh_install(ssh, "apt-package", package, retry=retry, logger=logger)


##


def setup_asset(
    asset_owner: str,
    asset_repo: str,
    path: PathLike,
    /,
    *,
    tag: str | None = None,
    token: Secret[str] | None = GITHUB_TOKEN,
    match_system: bool = False,
    match_c_std_lib: bool = False,
    match_machine: bool = False,
    not_matches: MaybeSequenceStr | None = None,
    not_endswith: MaybeSequenceStr | None = None,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
) -> None:
    """Setup a GitHub asset."""
    log_info(
        logger,
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
            f"{sudo=}",
            f"{perms=}",
            f"{owner=}",
            f"{group=}",
        ),
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
    ) as src:
        cp(src, path, sudo=sudo, perms=perms, owner=owner, group=group)
        log_info(logger, "Downloaded to %r", str(path))


##


def setup_age(
    *,
    ssh: str | None = None,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
) -> None:
    """Setup 'age'."""
    if ssh is None:
        with yield_gzip_asset(
            "FiloSottile",
            "age",
            token=token,
            match_system=True,
            match_machine=True,
            not_endswith=["proof"],
            chunk_size=chunk_size,
        ) as temp:
            downloads: list[Path] = []
            for src in temp.iterdir():
                if src.name.startswith("age"):
                    dest = Path(path_binaries, src.name)
                    cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
                    downloads.append(dest)
        log_info(logger, "Downloaded to %s", ", ".join(map(repr_str, downloads)))
    else:
        ssh_install(ssh, "age", retry=retry, logger=logger)


##


def setup_bat(
    *,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
) -> None:
    """Setup 'bat'."""
    with yield_gzip_asset(
        "sharkdp",
        "bat",
        token=token,
        match_system=True,
        match_c_std_lib=True,
        match_machine=True,
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "bat"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    log_info(logger, "Downloaded to %r", str(dest))


##


def setup_bottom(
    *,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
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
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "btm"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    log_info(logger, "Downloaded to %r", str(dest))


##


def setup_curl(
    *,
    ssh: str | None = None,
    sudo: bool = False,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
) -> None:
    """Setup 'curl'."""
    setup_apt_package("curl", ssh=ssh, sudo=sudo, retry=retry, logger=logger)


##


def setup_delta(
    *,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
) -> None:
    """Setup 'delta'."""
    with yield_gzip_asset(
        "dandavison",
        "delta",
        token=token,
        match_system=True,
        match_c_std_lib=True,
        match_machine=True,
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "delta"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    log_info(logger, "Downloaded to %r", str(dest))


##


def setup_direnv(
    *,
    ssh: str | None = None,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
    etc: bool = False,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
    __root: PathLike = FILE_SYSTEM_ROOT,
) -> None:
    """Setup 'direnv'."""
    if ssh is None:
        dest = Path(path_binaries, "direnv")
        setup_asset(
            "direnv",
            "direnv",
            dest,
            token=token,
            match_system=True,
            match_machine=True,
            chunk_size=chunk_size,
            sudo=sudo,
            perms=perms,
            owner=owner,
            group=group,
        )
        log_info(logger, "Downloaded to %r", str(dest))
        setup_shell_config(
            f'eval "$(direnv hook {SHELL})"',
            "direnv hook fish | source",
            etc="direnv" if etc else None,
            __root=__root,
        )
    else:
        ssh_install(ssh, "direnv", sudo=sudo, etc=etc, retry=retry, logger=logger)


##


def setup_docker(
    *,
    ssh: str | None = None,
    sudo: bool = False,
    user: str | None = None,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
) -> None:
    if ssh is None:
        match SYSTEM_NAME:
            case "Darwin":
                msg = f"Unsupported system: {SYSTEM_NAME!r}"
                raise ValueError(msg)
            case "Linux":
                if logger is not None:
                    to_logger(logger).info("Installing 'docker'...")
                try:
                    _ = which("docker")
                except WhichError:
                    apt_remove(
                        "docker.io",
                        "docker-doc",
                        "docker-compose",
                        "podman-docker",
                        "containerd",
                        "runc",
                        sudo=sudo,
                    )
                    apt_update(sudo=sudo)
                    apt_install("ca-certificates", "curl", sudo=sudo)
                    docker_asc = Path("/etc/apt/keyrings/docker.asc")
                    install(
                        docker_asc.parent,
                        directory=True,
                        mode="u=rwx,g=rx,o=rx",
                        sudo=sudo,
                    )
                    curl(
                        "https://download.docker.com/linux/debian/gpg",
                        output=docker_asc,
                        sudo=sudo,
                    )
                    chmod(docker_asc, "u=rw,g=r,o=r", sudo=sudo)
                    release = Path("/etc/os-release").read_text()
                    pattern = re.compile(r"^VERSION_CODENAME=(\w+)$")
                    line = one(
                        line for line in release.splitlines() if pattern.search(line)
                    )
                    codename = extract_group(pattern, line)
                    tee(
                        "/etc/apt/sources.list.d/docker.sources",
                        normalize_multi_line_str(f"""
                            Types: deb
                            URIs: https://download.docker.com/linux/debian
                            Suites: {codename}
                            Components: stable
                            Signed-By: /etc/apt/keyrings/docker.asc
                        """),
                        sudo=sudo,
                    )
                    apt_install(
                        "docker-ce",
                        "docker-ce-cli",
                        "containerd.io",
                        "docker-buildx-plugin",
                        "docker-compose-plugin",
                        update=True,
                        sudo=sudo,
                    )
                if user is not None:
                    run(*maybe_sudo_cmd("usermod", "-aG", "docker", user, sudo=sudo))
                if logger is not None:
                    to_logger(logger).info("Installing 'docker'...")
            case never:
                assert_never(never)
    else:
        args: list[str] = []
        if user is not None:
            args.extend(["--user", user])
        ssh_install(ssh, "docker", *args, retry=retry, logger=logger)


##


def setup_dust(
    *,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
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
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "dust"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    log_info(logger, "Downloaded to %r", str(dest))


##


def setup_eza(
    *,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
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
        chunk_size=chunk_size,
    ) as src:
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    log_info(logger, "Downloaded to %r", str(dest))


##


def setup_fd(
    *,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
) -> None:
    """Setup 'fd'."""
    with yield_gzip_asset(
        "sharkdp",
        "fd",
        token=token,
        match_system=True,
        match_c_std_lib=True,
        match_machine=True,
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "fd"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    log_info(logger, "Downloaded to %r", str(dest))


##


def setup_fzf(
    *,
    ssh: str | None = None,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
    etc: bool = False,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
    __root: PathLike = FILE_SYSTEM_ROOT,
) -> None:
    """Setup 'fzf'."""
    if ssh is None:
        with yield_gzip_asset(
            "junegunn",
            "fzf",
            token=token,
            match_system=True,
            match_machine=True,
            chunk_size=chunk_size,
        ) as src:
            dest = Path(path_binaries, src.name)
            cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
        log_info(logger, "Downloaded to %r", str(dest))
        setup_shell_config(
            'eval "$(fzf --bash)"',
            "fzf --fish | source",
            etc="fzf" if etc else None,
            zsh="source <(fzf --zsh)",
            __root=__root,
        )
    else:
        ssh_install(ssh, "fzf", sudo=sudo, etc=etc, retry=retry, logger=logger)


##


def setup_git(
    *,
    ssh: str | None = None,
    sudo: bool = False,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
) -> None:
    """Setup 'git'."""
    setup_apt_package("git", ssh=ssh, sudo=sudo, retry=retry, logger=logger)


##


def setup_jq(
    *,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
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
        chunk_size=chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
    )
    log_info(logger, "Downloaded to %r", str(dest))


##


def setup_just(
    *,
    ssh: str | None = None,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
) -> None:
    """Setup 'just'."""
    if ssh is None:
        with yield_gzip_asset(
            "casey",
            "just",
            token=token,
            match_system=True,
            match_machine=True,
            chunk_size=chunk_size,
        ) as temp:
            src = temp / "just"
            dest = Path(path_binaries, src.name)
            cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
        log_info(logger, "Downloaded to %r", str(dest))
    else:
        ssh_install(ssh, "just", retry=retry, logger=logger)


##


def setup_neovim(
    *,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
) -> None:
    """Setup 'neovim'."""
    with yield_gzip_asset(
        "neovim",
        "neovim",
        token=token,
        match_system=True,
        match_machine=True,
        not_endswith=["appimage", "zsync"],
        chunk_size=chunk_size,
    ) as temp:
        dest_dir = Path(path_binaries, "nvim-dir")
        cp(temp, dest_dir, sudo=sudo, perms=perms, owner=owner, group=group)
        dest_bin = Path(path_binaries, "nvim")
        symlink(dest_dir / "bin/nvim", dest_bin, sudo=sudo)
    log_info(logger, "Downloaded to %r", str(dest_bin))


##


def setup_restic(
    *,
    ssh: str | None = None,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
) -> None:
    """Setup 'restic'."""
    if ssh is None:
        with yield_bz2_asset(
            "restic",
            "restic",
            token=token,
            match_system=True,
            match_machine=True,
            chunk_size=chunk_size,
        ) as src:
            dest = Path(path_binaries, "restic")
            cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
        log_info(logger, "Downloaded to %r", str(dest))
    else:
        ssh_install(ssh, "restic", retry=retry, logger=logger)


##


def setup_ripgrep(
    *,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
) -> None:
    """Setup 'ripgrep'."""
    with yield_gzip_asset(
        "burntsushi",
        "ripgrep",
        token=token,
        match_system=True,
        match_machine=True,
        not_endswith=["sha256"],
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "rg"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    log_info(logger, "Downloaded to %r", str(dest))


##


def setup_starship(
    *,
    ssh: str | None = None,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
    etc: bool = False,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
    __root: PathLike = FILE_SYSTEM_ROOT,
) -> None:
    """Setup 'starship'."""
    if ssh is None:
        with yield_gzip_asset(
            "starship",
            "starship",
            token=token,
            match_system=True,
            match_c_std_lib=True,
            match_machine=True,
            not_endswith=["sha256"],
            chunk_size=chunk_size,
        ) as src:
            dest = Path(path_binaries, src.name)
            cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
        log_info(logger, "Downloaded to %r", str(dest))
        setup_shell_config(
            f'eval "$(starship init {SHELL})"',
            "starship init fish | source",
            etc="starship" if etc else None,
            __root=__root,
        )
    else:
        ssh_install(ssh, "starship", sudo=sudo, etc=etc, retry=retry, logger=logger)


##


def setup_taplo(
    *,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
) -> None:
    """Setup 'taplo'."""
    with yield_gzip_asset(
        "tamasfe",
        "taplo",
        token=token,
        match_system=True,
        match_machine=True,
        chunk_size=chunk_size,
    ) as src:
        dest = Path(path_binaries, "taplo")
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    log_info(logger, "Downloaded to %r", str(dest))


##


def setup_rsync(
    *,
    ssh: str | None = None,
    sudo: bool = False,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
) -> None:
    """Setup 'rsync'."""
    setup_apt_package("rsync", ssh=ssh, sudo=sudo, retry=retry, logger=logger)


##


def setup_ruff(
    *,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
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
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "ruff"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    log_info(logger, "Downloaded to %r", str(dest))


##


def setup_sd(
    *,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
) -> None:
    """Setup 'sd'."""
    with yield_gzip_asset(
        "chmln",
        "sd",
        token=token,
        match_system=True,
        match_c_std_lib=True,
        match_machine=True,
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "sd"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    log_info(logger, "Downloaded to %r", str(dest))


##


def setup_shellcheck(
    *,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
) -> None:
    """Setup 'shellcheck'."""
    with yield_gzip_asset(
        "koalaman",
        "shellcheck",
        token=token,
        match_system=True,
        match_machine=True,
        not_endswith=["tar.xz"],
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "shellcheck"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    log_info(logger, "Downloaded to %r", str(dest))


##


def setup_shfmt(
    *,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
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
        chunk_size=chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
    )
    log_info(logger, "Downloaded to %r", str(dest))


##


def setup_sops(
    *,
    ssh: str | None = None,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
) -> None:
    """Setup 'sops'."""
    if ssh is None:
        dest = Path(path_binaries, "sops")
        setup_asset(
            "getsops",
            "sops",
            dest,
            token=token,
            match_system=True,
            match_machine=True,
            not_endswith=["json"],
            chunk_size=chunk_size,
            sudo=sudo,
            perms=perms,
            owner=owner,
            group=group,
        )
        log_info(logger, "Downloaded to %r", str(dest))
    else:
        ssh_install(ssh, "sops", retry=retry, logger=logger)


##


def setup_uv(
    *,
    ssh: str | None = None,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
) -> None:
    """Setup 'uv'."""
    if ssh is None:
        with yield_gzip_asset(
            "astral-sh",
            "uv",
            token=token,
            match_system=True,
            match_c_std_lib=True,
            match_machine=True,
            not_endswith=["sha256"],
            chunk_size=chunk_size,
        ) as temp:
            src = temp / "uv"
            dest = Path(path_binaries, src.name)
            cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
        log_info(logger, "Downloaded to %r", str(dest))
    else:
        user, hostname = split_ssh(ssh)
        with yield_ssh_temp_dir(user, hostname, retry=retry, logger=logger) as temp:
            path = temp / "install.sh"
            cmds: list[list[str]] = [
                curl_cmd("https://astral.sh/uv/install.sh", output=path),
                maybe_sudo_cmd(
                    "env",
                    f"UV_INSTALL_DIR={path_binaries}",
                    "UV_NO_MODIFY_PATH=1",
                    "sh",
                    str(path),
                    sudo=sudo,
                ),
            ]
            utilities.subprocess.ssh(
                user,
                hostname,
                *BASH_LS,
                input="\n".join(map(join, cmds)),
                retry=retry,
                logger=logger,
            )
        log_info(logger, "Downloaded to %r on '%s'", str(path_binaries), hostname)


##


def setup_watchexec(
    *,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
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
        chunk_size=chunk_size,
    ) as temp:
        src = temp / "watchexec"
        dest = Path(path_binaries, src.name)
        cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
    log_info(logger, "Downloaded to %r", str(dest))


##


def setup_yq(
    *,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
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
        chunk_size=chunk_size,
        sudo=sudo,
        perms=perms,
        owner=owner,
        group=group,
    )
    log_info(logger, "Downloaded to %r", str(dest))


##


def setup_zoxide(
    *,
    ssh: str | None = None,
    token: Secret[str] | None = GITHUB_TOKEN,
    path_binaries: PathLike = PATH_BINARIES,
    sudo: bool = False,
    perms: PermissionsLike | None = None,
    owner: str | int | None = None,
    group: str | int | None = None,
    etc: bool = False,
    retry: Retry | None = None,
    logger: LoggerLike | None = None,
    __root: PathLike = FILE_SYSTEM_ROOT,
) -> None:
    """Setup 'zoxide'."""
    if ssh is None:
        with yield_gzip_asset(
            "ajeetdsouza",
            "zoxide",
            token=token,
            match_system=True,
            match_machine=True,
            chunk_size=chunk_size,
        ) as temp:
            src = temp / "zoxide"
            dest = Path(path_binaries, src.name)
            cp(src, dest, sudo=sudo, perms=perms, owner=owner, group=group)
        log_info(logger, "Downloaded to %r", str(dest))
        setup_shell_config(
            f'eval "$(fzf --{SHELL})"',
            "zoxide init fish | source",
            etc="zoxide" if etc else None,
            __root=__root,
        )
    else:
        ssh_install(ssh, "zoxide", sudo=sudo, etc=etc, retry=retry, logger=logger)


__all__ = [
    "setup_age",
    "setup_apt_package",
    "setup_asset",
    "setup_bat",
    "setup_bottom",
    "setup_curl",
    "setup_delta",
    "setup_direnv",
    "setup_docker",
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
