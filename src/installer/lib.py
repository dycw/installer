from __future__ import annotations

import gzip
from collections.abc import Iterable, Mapping
from logging import getLogger
from os import environ
from pathlib import Path
from re import search
from shutil import copyfileobj, which
from typing import TYPE_CHECKING, Any, assert_never
from zipfile import ZipFile

from .constants import (
    AUTHORIZED_KEYS,
    BASHRC,
    CONFIG_BOTTOM_TOML,
    CONFIG_DIRENV,
    CONFIG_FD_IGNORE,
    CONFIG_FISH,
    CONFIG_FISH_CONF_D,
    CONFIG_FISH_FUNCTIONS,
    CONFIG_GIT,
    CONFIG_GLAB_CONFIG_YML,
    CONFIG_NVIM,
    CONFIG_SOPS_AGE,
    CONFIG_STARSHIP_TOML,
    CONFIG_TMUX_CONF_LOCAL,
    CONFIG_TMUX_CONF_OH_MY_TMUX,
    CONFIG_WEZTERM_LUA,
    KNOWN_HOSTS,
    LOCAL_BIN,
    PDBRC,
    PSQLRC,
    RESOLV_CONF,
    SSH_CONFIG,
    SSH_CONFIG_D,
)
from .enums import System
from .utilities import (
    TemporaryDirectory,
    apt_install,
    brew_install,
    brew_installed,
    check_for_commands,
    chmod,
    contains_line,
    cp,
    dpkg_install,
    full_path,
    have_command,
    luarocks_install,
    mac_app_exists,
    mkdir,
    replace_lines,
    run_command,
    run_commands,
    symlink,
    uv_tool_install,
    write_template,
    write_text,
    yield_download,
    yield_github_latest_download,
)

if TYPE_CHECKING:
    from .types import PathLike


_LOGGER = getLogger(__name__)


def add_to_known_hosts() -> None:
    if contains_line(KNOWN_HOSTS, r"github\.com"):
        _LOGGER.debug("Known hosts already contains 'github.com'")
        return
    _LOGGER.info("Adding 'github.com' to known hosts...")
    mkdir(KNOWN_HOSTS.parent, ownership=True)
    _ = run_command(f"ssh-keyscan github.com >> {KNOWN_HOSTS}")


def install_age() -> None:
    if have_command("age"):
        _LOGGER.debug("'age' is already installed")
        return
    _LOGGER.info("Installing 'age'...")
    match System.identify():
        case System.mac:
            brew_install("age")
        case System.linux:
            apt_install("age")
        case never:
            assert_never(never)


def install_agg() -> None:
    if have_command("agg"):
        _LOGGER.debug("'agg' is already installed")
        return
    _LOGGER.info("Installing 'agg'...")
    match System.identify():
        case System.mac:
            brew_install("agg")
        case System.linux:
            path_to = LOCAL_BIN / "agg"
            with yield_github_latest_download(
                "asciinema", "agg", "agg-x86_64-unknown-linux-gnu"
            ) as binary:
                cp(binary, path_to, executable=True, ownership=True)
        case never:
            assert_never(never)


def install_asciinema() -> None:
    if have_command("asciinema"):
        _LOGGER.debug("'asciinema' is already installed")
        return
    _LOGGER.info("Installing 'asciinema'...")
    match System.identify():
        case System.mac:
            brew_install("asciinema")
        case System.linux:
            apt_install("asciinema")
        case never:
            assert_never(never)


def install_bat() -> None:
    match System.identify():
        case System.mac:
            if have_command("bat"):
                _LOGGER.debug("'bat' is already installed")
                return
            _LOGGER.info("Installing 'bat'...")
            brew_install("bat")
        case System.linux:
            if have_command("batcat"):
                _LOGGER.debug("'bat' is already installed")
            else:
                _LOGGER.info("Installing 'bat'...")
                apt_install("bat")
            if (path_to := which("batcat")) is None:
                msg = "'batcat' should be installed"
                raise RuntimeError(msg)
            symlink(LOCAL_BIN / "bat", path_to)
        case never:
            assert_never(never)


def install_bottom(*, bottom_toml: PathLike | None = None) -> None:
    if have_command("btm"):
        _LOGGER.debug("'bottom' is already installed")
    else:
        _LOGGER.info("Installing 'bottom'...")
        match System.identify():
            case System.mac:
                brew_install("bottom")
            case System.linux:
                with yield_github_latest_download(
                    "clementtsang", "bottom", "bottom_${tag}-1_amd64.deb"
                ) as dpkg:
                    dpkg_install(dpkg)
            case never:
                assert_never(never)
    if bottom_toml is not None:
        symlink(CONFIG_BOTTOM_TOML, bottom_toml)


def install_build_essential() -> None:
    if have_command("cc"):
        _LOGGER.debug(
            "'cc' is already installed (and presumably so is 'build-essential'"
        )
        return
    _LOGGER.info("Installing 'build-essential'...")
    apt_install("build-essential")


def install_bump_my_version() -> None:
    if have_command("bump-my-version"):
        _LOGGER.debug("'bump-my-version' is already installed")
        return
    _LOGGER.info("Installing 'bump-my-version'...")
    match System.identify():
        case System.mac:
            brew_install("bump-my-version")
        case System.linux:
            uv_tool_install("bump-my-version")
        case never:
            assert_never(never)


def install_brew() -> None:
    if have_command("brew"):
        _LOGGER.debug("'brew' is already installed")
        return
    _LOGGER.info("Installing 'brew'...")
    check_for_commands("curl")
    _ = run_command(
        "curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | bash",
        env={"NONINTERACTIVE": "1"},
    )


def install_curl() -> None:
    if have_command("curl"):
        _LOGGER.debug("'curl' is already installed")
        return
    _LOGGER.info("Installing 'curl'...")
    apt_install("curl")


def install_delta() -> None:
    if have_command("delta"):
        _LOGGER.debug("'delta' is already installed")
        return
    _LOGGER.info("Installing 'delta'...")
    match System.identify():
        case System.mac:
            brew_install("git-delta")
        case System.linux:
            with yield_github_latest_download(
                "dandavison", "delta", "git-delta_${tag}_amd64.deb"
            ) as dpkg:
                dpkg_install(dpkg)
        case never:
            assert_never(never)


def install_direnv(
    *, direnv_toml: PathLike | None = None, direnvrc: PathLike | None = None
) -> None:
    if have_command("direnv"):
        _LOGGER.debug("'direnv' is already installed")
    else:
        _LOGGER.info("Installing 'direnv'...")
        match System.identify():
            case System.mac:
                brew_install("direnv")
            case System.linux:
                check_for_commands("curl")
                setup_local_bin()
                _ = run_command(
                    "curl -sfL https://direnv.net/install.sh | bash",
                    env={"bin_path": str(LOCAL_BIN)},
                )
            case never:
                assert_never(never)
    if direnv_toml is not None:
        symlink(CONFIG_DIRENV / "direnv.toml", direnv_toml)
    if direnvrc is not None:
        symlink(CONFIG_DIRENV / "direnvrc", direnvrc)


def install_docker() -> None:
    if have_command("docker"):
        _LOGGER.debug("'docker' is already installed")
    else:
        _LOGGER.info("Installing 'docker'...")
        match System.identify():
            case System.mac:
                brew_install("docker")
            case System.linux:
                check_for_commands("curl")
                packages = [
                    "docker.io",
                    "docker-doc",
                    "docker-compose",
                    "podman-docker",
                    "containerd",
                    "runc",
                ]
                _ = run_commands(*(f"sudo apt-get remove {p}" for p in packages))
                apt_install("ca-certificates", "curl")
                _ = run_commands(
                    "sudo install -m 0755 -d /etc/apt/keyrings",
                    "sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc",
                    "sudo chmod a+r /etc/apt/keyrings/docker.asc",
                    'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null',
                )
                apt_install(
                    "docker-ce",
                    "docker-ce-cli",
                    "containerd.io",
                    "docker-buildx-plugin",
                    "docker-compose-plugin",
                )
            case never:
                assert_never(never)
    _ = run_command("sudo usermod -aG docker $USER")


def install_dropbox() -> None:
    if brew_installed("dropbox"):
        _LOGGER.debug("'dropbox' is already installed")
        return
    _LOGGER.info("Installing 'dropbox'...")
    brew_install("dropbox", cask=True)


def install_dust() -> None:
    if have_command("dust"):
        _LOGGER.debug("'dust' is already installed")
        return
    _LOGGER.info("Installing 'delta'...")
    match System.identify():
        case System.mac:
            brew_install("dust")
        case System.linux:
            apt_install("du-dust")
        case never:
            assert_never(never)


def install_eza() -> None:
    if have_command("eza"):
        _LOGGER.debug("'eza' is already installed")
        return
    _LOGGER.info("Installing 'eza'...")
    match System.identify():
        case System.mac:
            brew_install("eza")
        case System.linux:
            apt_install("eza")
        case never:
            assert_never(never)


def install_fd(*, ignore: PathLike | None = None) -> None:
    if have_command("fd"):
        _LOGGER.debug("'fd-find' is already installed")
    else:
        _LOGGER.info("Installing 'fd-find'...")
        match System.identify():
            case System.mac:
                brew_install("fd")
            case System.linux:
                apt_install("fd-find")
            case never:
                assert_never(never)
    if System.identify() is System.linux:
        if (path_to := which("fdfind")) is None:
            msg = "'fdfind' should be installed"
            raise RuntimeError(msg)
        symlink(LOCAL_BIN / "fd", path_to)
    if ignore is not None:
        symlink(CONFIG_FD_IGNORE, ignore)


def install_fish(
    *,
    config: PathLike | None = None,
    env: PathLike | None = None,
    git: PathLike | None = None,
    work: PathLike | None = None,
) -> None:
    if have_command("fish"):
        _LOGGER.debug("'fish' is already installed")
    else:
        _LOGGER.info("Installing 'fish'...")
        match System.identify():
            case System.mac:
                brew_install("fish")
            case System.linux:
                check_for_commands("curl")
                _ = run_commands(
                    "echo 'deb http://download.opensuse.org/repositories/shells:/fish/Debian_13/ /' | sudo tee /etc/apt/sources.list.d/shells:fish.list",
                    "curl -fsSL https://download.opensuse.org/repositories/shells:fish/Debian_13/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/shells_fish.gpg > /dev/null",
                )
                apt_install("fish")
            case never:
                assert_never(never)
    if search(r"/fish$", environ["SHELL"]):
        _LOGGER.debug("'fish' is already the default shell")
    else:
        _LOGGER.info("Setting 'fish' as the default shell...")
        _ = run_commands("sudo chsh -s $(which fish)")
    if config is not None:
        symlink(CONFIG_FISH / "config.fish", config)
    if env is not None:
        symlink(CONFIG_FISH_CONF_D / "0-env.fish", env)
    if git is not None:
        symlink(CONFIG_FISH_CONF_D / "git.fish", git)
    if work is not None:
        symlink(CONFIG_FISH_CONF_D / "work.fish", work)


def install_fzf(*, fzf_fish: PathLike | None = None) -> None:
    if have_command("fzf"):
        _LOGGER.debug("'fzf' is already installed")
    else:
        _LOGGER.info("Installing 'fzf'...")
        match System.identify():
            case System.mac:
                brew_install("fzf")
            case System.linux:
                apt_install("fzf")
            case never:
                assert_never(never)
    if fzf_fish is not None:
        for path in (full_path(fzf_fish) / "functions").iterdir():
            cp(path, CONFIG_FISH_FUNCTIONS / path.name, ownership=True)


def install_ggrep() -> None:
    if have_command("ggrep"):
        _LOGGER.debug("'ggrep' is already installed")
    else:
        _LOGGER.info("Installing 'ggrep'...")
        brew_install("grep")
    if (path_to := which("ggrep")) is None:
        msg = "'ggrep' should be installed"
        raise RuntimeError(msg)
    symlink(LOCAL_BIN / "grep", path_to)


def install_gh() -> None:
    if have_command("gh"):
        _LOGGER.debug("'gh' is already installed")
        return
    _LOGGER.info("Installing 'gh'...")
    match System.identify():
        case System.mac:
            brew_install("gh")
        case System.linux:
            apt_install("gh")
        case never:
            assert_never(never)


def install_ghostty() -> None:
    if have_command("ghostty"):
        _LOGGER.debug("'ghostty' is already installed")
        return
    _LOGGER.info("Installing 'ghostty'...")
    match System.identify():
        case System.mac:
            brew_install("ghostty", cask=True)
        case System.linux:
            check_for_commands("curl")
            _ = run_command(
                'curl -sS https://debian.griffo.io/EA0F721D231FDD3A0A17B9AC7808B4DD62C41256.asc | sudo gpg --dearmor --yes -o /etc/apt/trusted.gpg.d/debian.griffo.io.gpg echo "deb https://debian.griffo.io/apt $(lsb_release -sc 2>/dev/null) main" | sudo tee /etc/apt/sources.list.d/debian.griffo.io.list'
            )
            apt_install(
                "zig",
                "ghostty",
                "lazygit",
                "yazi",
                "eza",
                "uv",
                "fzf",
                "zoxide",
                "bun",
                "tigerbeetle",
            )
        case never:
            assert_never(never)


def install_git(
    *, config: PathLike | None = None, ignore: PathLike | None = None
) -> None:
    if have_command("git"):
        _LOGGER.debug("'git' is already installed")
    else:
        _LOGGER.info("Installing 'git'...")
        match System.identify():
            case System.mac:
                msg = "Mac should already have 'git' installed"
                raise RuntimeError(msg)
            case System.linux:
                apt_install("git")
            case never:
                assert_never(never)
    if config is not None:
        symlink(CONFIG_GIT / "config", config)
    if ignore is not None:
        symlink(CONFIG_GIT / "ignore", ignore)


def install_gitweb() -> None:
    if have_command("gitweb"):
        _LOGGER.debug("'gitweb' is already installed")
        return
    _LOGGER.info("Installing 'gitweb'...")
    match System.identify():
        case System.mac:
            brew_install("yoannfleurydev/gitweb/gitweb")
        case System.linux:
            path_to = LOCAL_BIN / "gitweb"
            with yield_github_latest_download(
                "yoannfleurydev", "gitweb", "gitweb-linux"
            ) as binary:
                cp(binary, path_to, executable=True, ownership=True)
        case never:
            assert_never(never)


def install_glab(*, config_yml: PathLike | None = None) -> None:
    if have_command("glab"):
        _LOGGER.debug("'glab' is already installed")
    else:
        _LOGGER.info("Installing 'glab'...")
        match System.identify():
            case System.mac:
                brew_install("glab")
            case System.linux:
                apt_install("glab")
            case never:
                assert_never(never)
    if config_yml is not None:
        cp(CONFIG_GLAB_CONFIG_YML, config_yml, ownership=True)


def install_gsed() -> None:
    if have_command("gsed"):
        _LOGGER.debug("'gsed' is already installed")
    else:
        _LOGGER.info("Installing 'gsed'...")
        brew_install("gnu-sed")
    if (path_to := which("gsed")) is None:
        msg = "'gsed' should be installed"
        raise RuntimeError(msg)
    symlink(LOCAL_BIN / "sed", path_to)


def install_iperf3() -> None:
    if have_command("iperf3"):
        _LOGGER.debug("'iperf3' is already installed")
        return
    _LOGGER.info("Installing 'iperf3'...")
    match System.identify():
        case System.mac:
            brew_install("iperf3")
        case System.linux:
            apt_install("iperf3", non_interactive=True)
        case never:
            assert_never(never)


def install_jq() -> None:
    if have_command("jq"):
        _LOGGER.debug("'jq' is already installed")
        return
    _LOGGER.info("Installing 'jq'...")
    match System.identify():
        case System.mac:
            brew_install("jq")
        case System.linux:
            apt_install("jq")
        case never:
            assert_never(never)


def install_just() -> None:
    if have_command("just"):
        _LOGGER.debug("'just' is already installed")
        return
    _LOGGER.info("Installing 'just'...")
    match System.identify():
        case System.mac:
            brew_install("just")
        case System.linux:
            apt_install("just")
        case never:
            assert_never(never)


def install_libpq() -> None:
    if brew_installed("libpq"):
        _LOGGER.debug("'libpq' is already installed")
        return
    _LOGGER.info("Installing 'libpq'...")
    brew_install("libpq")
    _ = run_command("brew link --force libpq")


def install_luacheck() -> None:
    if have_command("luacheck"):
        _LOGGER.debug("'luacheck' is already installed")
        return
    _LOGGER.info("Installing 'luacheck'...")
    match System.identify():
        case System.mac:
            brew_install("luacheck")
        case System.linux:
            luarocks_install("luacheck")
        case never:
            assert_never(never)


def install_luarocks() -> None:
    if have_command("luarocks"):
        _LOGGER.debug("'luarocks' is already installed")
        return
    _LOGGER.info("Installing 'luarocks'...")
    match System.identify():
        case System.mac:
            brew_install("luarocks")
        case System.linux:
            apt_install("luarocks")
        case never:
            assert_never(never)


def install_maturin() -> None:
    if have_command("maturin"):
        _LOGGER.debug("'maturin' is already installed")
        return
    _LOGGER.info("Installing 'maturin'...")
    match System.identify():
        case System.mac:
            brew_install("maturin")
        case System.linux:
            uv_tool_install("maturin")
        case never:
            assert_never(never)


def install_neovim(*, nvim_dir: PathLike | None = None) -> None:
    if have_command("nvim"):
        _LOGGER.debug("'neovim' is already installed")
    else:
        _LOGGER.info("Installing 'neovim'...")
        match System.identify():
            case System.mac:
                brew_install("neovim")
            case System.linux:
                apt_install("fuse")
                path_to = LOCAL_BIN / "nvim"
                with yield_download(
                    "https://github.com/neovim/neovim/releases/download/stable/nvim-linux-x86_64.appimage"
                ) as appimage:
                    cp(appimage, path_to, executable=True, ownership=True)
            case never:
                assert_never(never)
    if nvim_dir is not None:
        symlink(CONFIG_NVIM, nvim_dir)
    _ = run_command("nvim --headless '+Lazy! sync' +qa", direnv=True)


def install_neovim_dependencies() -> None:
    if have_command("npm"):
        _LOGGER.debug("'npm' is already installed")
    else:
        _LOGGER.info("Installing 'npm'...")
        apt_install("nodejs", "npm")
    if have_command("python3.13"):
        _LOGGER.debug(
            "'python3.13' is already installed (and presumably so is 'python3.13-venv')"
        )
    else:
        _LOGGER.info("Installing 'python3.13-venv'...")
        apt_install("python3.13-venv")


def install_postico() -> None:
    if mac_app_exists("Postico 2"):
        _LOGGER.debug("'postico' is already installed")
        return
    _LOGGER.info("Installing 'postico'...")
    brew_install("postico", cask=True)


def install_pre_commit() -> None:
    if have_command("pre-commit"):
        _LOGGER.debug("'pre-commit' is already installed")
        return
    _LOGGER.info("Installing 'pre-commit'...")
    match System.identify():
        case System.mac:
            brew_install("pre-commit")
        case System.linux:
            uv_tool_install("pre-commit")
        case never:
            assert_never(never)


def install_protonvpn() -> None:
    if brew_installed("protonvpn"):
        _LOGGER.debug("'protonvpn' is already installed")
        return
    _LOGGER.info("Installing 'protonvpn'...")
    brew_install("protonvpn", cask=True)


def install_pyright() -> None:
    if have_command("pyright"):
        _LOGGER.debug("'pyright' is already installed")
        return
    _LOGGER.info("Installing 'pyright'...")
    match System.identify():
        case System.mac:
            brew_install("pyright")
        case System.linux:
            uv_tool_install("pyright")
        case never:
            assert_never(never)


def install_restic() -> None:
    if have_command("restic"):
        _LOGGER.debug("'restic' is already installed")
        return
    _LOGGER.info("Installing 'restic'...")
    match System.identify():
        case System.mac:
            brew_install("restic")
        case System.linux:
            apt_install("restic")
        case never:
            assert_never(never)


def install_ripgrep(*, ripgreprc: PathLike | None = None) -> None:
    if have_command("rg"):
        _LOGGER.debug("'ripgrep' is already installed")
    else:
        _LOGGER.info("Installing 'ripgrep'...")
        apt_install("ripgrep")
    path_from = environ.get("RIPGREP_CONFIG_PATH")
    if (path_from is not None) and (ripgreprc is not None):
        symlink(path_from, ripgreprc)


def install_rlwrap() -> None:
    if have_command("rlwrap"):
        _LOGGER.debug("'rlwrap' is already installed")
        return
    _LOGGER.info("Installing 'rlwrap'...")
    brew_install("rlwrap")


def install_rsync() -> None:
    if have_command("rsync"):
        _LOGGER.debug("'rsync' is already installed")
        return
    _LOGGER.info("Installing 'rsync'...")
    apt_install("rsync")


def install_ruff() -> None:
    if have_command("ruff"):
        _LOGGER.debug("'ruff' is already installed")
        return
    _LOGGER.info("Installing 'ruff'...")
    match System.identify():
        case System.mac:
            brew_install("ruff")
        case System.linux:
            uv_tool_install("ruff")
        case never:
            assert_never(never)


def install_shellcheck() -> None:
    if have_command("shellcheck"):
        _LOGGER.debug("'shellcheck' is already installed")
        return
    _LOGGER.info("Installing 'shellcheck'...")
    match System.identify():
        case System.mac:
            brew_install("shellcheck")
        case System.linux:
            apt_install("shellcheck")
        case never:
            assert_never(never)


def install_shfmt() -> None:
    if have_command("shfmt"):
        _LOGGER.debug("'shfmt' is already installed")
        return
    _LOGGER.info("Installing 'shfmt'...")
    match System.identify():
        case System.mac:
            brew_install("shfmt")
        case System.linux:
            apt_install("shfmt")
        case never:
            assert_never(never)


def install_sops(*, age_secret_key: PathLike | None = None) -> None:
    if have_command("sops"):
        _LOGGER.debug("'sops' is already installed")
    else:
        _LOGGER.info("Installing 'sops'...")
        match System.identify():
            case System.mac:
                brew_install("sops")
            case System.linux:
                path_to = LOCAL_BIN / "sops"
                with yield_github_latest_download(
                    "getsops", "sops", "sops-${tag}.linux.amd64"
                ) as binary:
                    cp(binary, path_to, executable=True, ownership=True)
            case never:
                assert_never(never)
    if age_secret_key is not None:
        symlink(CONFIG_SOPS_AGE, age_secret_key)


def install_spotify() -> None:
    match System.identify():
        case System.mac:
            if brew_installed("spotify"):
                _LOGGER.debug("'spotify' is already installed")
                return
            _LOGGER.info("Installing 'spotify'...")
            brew_install("spotify", cask=True)
        case System.linux:
            if have_command("spotify"):
                _LOGGER.debug("'spotify' is already installed")
                return
            check_for_commands("curl")
            _ = run_commands(
                "curl -sS https://download.spotify.com/debian/pubkey_C85668DF69375001.gpg | sudo gpg --dearmor --yes -o /etc/apt/trusted.gpg.d/spotify.gpg",
                'echo "deb https://repository.spotify.com stable non-free" | sudo tee /etc/apt/sources.list.d/spotify.list',
            )
            apt_install("spotify-client")
        case never:
            assert_never(never)


def install_starship(*, starship_toml: PathLike | None = None) -> None:
    if have_command("starship"):
        _LOGGER.debug("'starship' is already installed")
    else:
        _LOGGER.info("Installing 'starship'...")
        match System.identify():
            case System.mac:
                brew_install("starship")
            case System.linux:
                check_for_commands("curl")
                setup_local_bin()
                _ = run_command(
                    f"curl -sS https://starship.rs/install.sh | sh -s -- -b {LOCAL_BIN} -y"
                )
            case never:
                assert_never(never)
    if starship_toml is not None:
        symlink(CONFIG_STARSHIP_TOML, starship_toml)


def install_stylua() -> None:
    if have_command("stylua"):
        _LOGGER.debug("'stylua' is already installed")
        return
    _LOGGER.info("Installing 'stylua'...")
    match System.identify():
        case System.mac:
            brew_install("stylua")
        case System.linux:
            path_to = LOCAL_BIN / "stylua"
            with (
                yield_github_latest_download(
                    "johnnymorganz", "stylua", "stylua-linux-x86_64.zip"
                ) as zf,
                ZipFile(zf) as zfh,
                TemporaryDirectory() as temp_dir,
            ):
                zfh.extractall(temp_dir)
                (path_from,) = temp_dir.iterdir()
                cp(path_from, path_to, executable=True, ownership=True)
        case never:
            assert_never(never)


def install_syncthing() -> None:
    if have_command("syncthing"):
        _LOGGER.debug("'syncthing' is already installed")
        return
    _LOGGER.info("Installing 'syncthing'...")
    match System.identify():
        case System.mac:
            brew_install("syncthing")
        case System.linux:
            apt_install("syncthing")
        case never:
            assert_never(never)


def install_tailscale(*, auth_key: PathLike | None = None) -> None:
    if have_command("tailscale"):
        _LOGGER.debug("'tailscale' is already installed")
    else:
        _LOGGER.info("Installing 'tailscale'...")
        match System.identify():
            case System.mac:
                brew_install("syncthing")
            case System.linux:
                check_for_commands("curl")
                _ = run_command("curl -fsSL https://tailscale.com/install.sh | sh")
            case never:
                assert_never(never)
    try:
        path_from = environ["TAILSCALE_AUTH_KEY"]
    except KeyError:
        pass
    else:
        if isinstance(auth_key, Path) or (
            isinstance(auth_key, str) and full_path(auth_key).exists()
        ):
            symlink(path_from, auth_key)
        elif isinstance(auth_key, str):
            with TemporaryDirectory() as temp_dir:
                temp_file = temp_dir.joinpath("auth-key.txt")
                _ = temp_file.write_text(auth_key)
                symlink(path_from, temp_dir)


def install_taplo() -> None:
    if have_command("taplo"):
        _LOGGER.debug("'taplo' is already installed")
        return
    _LOGGER.info("Installing 'taplo'...")
    match System.identify():
        case System.mac:
            brew_install("taplo")
        case System.linux:
            path_to = LOCAL_BIN / "taplo"
            with (
                yield_github_latest_download(
                    "tamasfe", "taplo", "taplo-linux-x86_64.gz"
                ) as binary_gz,
                gzip.open(binary_gz) as fh_in,
                path_to.open(mode="wb") as fh_out,
            ):
                copyfileobj(fh_in, fh_out)
            chmod(path_to)
        case never:
            assert_never(never)


def install_tmux(
    *,
    tmux_conf_oh_my_tmux: PathLike | None = None,
    tmux_conf_local: PathLike | None = None,
) -> None:
    if have_command("tmux"):
        _LOGGER.debug("'tmux' is already installed")
    else:
        _LOGGER.info("Installing 'tmux'...")
        match System.identify():
            case System.mac:
                brew_install("tmux")
            case System.linux:
                apt_install("tmux")
            case never:
                assert_never(never)
    if tmux_conf_oh_my_tmux is not None:
        symlink(CONFIG_TMUX_CONF_OH_MY_TMUX, tmux_conf_oh_my_tmux)
    if tmux_conf_local is not None:
        symlink(CONFIG_TMUX_CONF_LOCAL, tmux_conf_local)


def install_topgrade() -> None:
    if have_command("topgrade"):
        _LOGGER.debug("'topgrade' is already installed")
        return
    _LOGGER.info("Installing 'topgrade'...")
    match System.identify():
        case System.mac:
            brew_install("topgrade")
        case System.linux:
            with yield_github_latest_download(
                "topgrade-rs", "topgrade", "topgrade_${tag_without_v}-1_amd64.deb"
            ) as dpkg:
                dpkg_install(dpkg)
        case never:
            assert_never(never)


def install_transmission() -> None:
    if brew_installed("transmission"):
        _LOGGER.debug("'transmission' is already installed")
        return
    _LOGGER.info("Installing 'transmission'...")
    brew_install("transmission", cask=True)


def install_uv() -> None:
    if have_command("uv"):
        _LOGGER.debug("'uv' is already installed")
        return
    _LOGGER.info("Installing 'uv'...")
    match System.identify():
        case System.mac:
            brew_install("uv")
        case System.linux:
            check_for_commands("curl")
            _ = run_command(
                "curl -LsSf https://astral.sh/uv/install.sh | sh -s",
                env={"UV_NO_MODIFY_PATH": "1"},
            )
        case never:
            assert_never(never)


def install_vim() -> None:
    if have_command("vim"):
        _LOGGER.debug("'vim' is already installed")
        return
    _LOGGER.info("Installing 'vim'...")
    match System.identify():
        case System.mac:
            brew_install("vim")
        case System.linux:
            apt_install("vim")
        case never:
            assert_never(never)


def install_vlc() -> None:
    if have_command("vlc"):
        _LOGGER.debug("'vlc' is already installed")
        return
    _LOGGER.info("Installing 'vlc'...")
    brew_install("vlc", cask=True)


def install_vs_code() -> None:
    if have_command("code"):
        _LOGGER.debug("'VS code' is already installed")
        return
    _LOGGER.info("Installing 'VS code'...")
    brew_install("visual-studio-code", cask=True)


def install_watch() -> None:
    if have_command("watch"):
        _LOGGER.debug("'watch' is already installed")
        return
    _LOGGER.info("Installing 'watch'...")
    brew_install("watch")


def install_watchexec() -> None:
    if have_command("watchexec"):
        _LOGGER.debug("'watchexec' is already installed")
        return
    _LOGGER.info("Installing 'watchexec'...")
    match System.identify():
        case System.mac:
            brew_install("watchexec")
        case System.linux:
            apt_install("watchexec-cli")
        case never:
            assert_never(never)


def install_wezterm(*, wezterm_lua: PathLike | None = None) -> None:
    if have_command("wezterm"):
        _LOGGER.debug("'wezterm' is already installed")
    else:
        _LOGGER.info("Installing 'wezterm'...")
        match System.identify():
            case System.mac:
                brew_install("wezterm", cask=True)
            case System.linux:
                check_for_commands("curl")
                _ = run_commands(
                    "curl -fsSL https://apt.fury.io/wez/gpg.key | sudo gpg --yes --dearmor -o /usr/share/keyrings/wezterm-fury.gpg",
                    "echo 'deb [signed-by=/usr/share/keyrings/wezterm-fury.gpg] https://apt.fury.io/wez/ * *' | sudo tee /etc/apt/sources.list.d/wezterm.list",
                    "sudo chmod 644 /usr/share/keyrings/wezterm-fury.gpg",
                )
                apt_install("wezterm")
            case never:
                assert_never(never)
    if wezterm_lua is not None:
        symlink(CONFIG_WEZTERM_LUA, wezterm_lua)


def install_whatsapp() -> None:
    if brew_installed("whatsapp"):
        _LOGGER.debug("'whatsapp' is already installed")
        return
    _LOGGER.info("Installing 'whatsapp'...")
    brew_install("whatsapp", cask=True)


def install_xclip() -> None:
    if have_command("xclip"):
        _LOGGER.debug("'xclip' is already installed")
        return
    _LOGGER.info("Installing 'xclip'...")
    apt_install("xclip")


def install_yq() -> None:
    if have_command("yq"):
        _LOGGER.debug("'yq' is already installed")
        return
    _LOGGER.info("Installing 'yq'...")
    match System.identify():
        case System.mac:
            brew_install("yq")
        case System.linux:
            path_to = LOCAL_BIN / "yq"
            with yield_github_latest_download(
                "mikefarah", "yq", "yq_linux_amd64"
            ) as binary:
                cp(binary, path_to, executable=True, ownership=True)
        case never:
            assert_never(never)


def install_zoxide() -> None:
    if have_command("zoxide"):
        _LOGGER.debug("'zoxide' is already installed")
        return
    _LOGGER.info("Installing 'zoxide'...")
    match System.identify():
        case System.mac:
            brew_install("zoxide")
        case System.linux:
            apt_install("zoxide")
        case never:
            assert_never(never)


def install_zoom(*, deb_file: PathLike | None = None) -> None:
    match System.identify():
        case System.mac:
            if brew_installed("zoom"):
                _LOGGER.debug("'zoom' is already installed")
                return
            _LOGGER.info("Installing 'zoom'...")
            brew_install("zoom", cask=True)
        case System.linux:
            if have_command("zoom"):
                _LOGGER.debug("'zoom' is already installed")
                return
            apt_install("libxcb-xinerama0", "libxcb-xtest0", "libxcb-cursor0")
            if deb_file is None:
                msg = "deb_file"
                raise FileNotFoundError(msg)
            dpkg_install(deb_file)
        case never:
            assert_never(never)


def setup_bashrc(*, bashrc: PathLike | None = None) -> None:
    if bashrc is not None:
        symlink(BASHRC, bashrc)


def setup_local_bin() -> None:
    mkdir(LOCAL_BIN, ownership=True)


def setup_pdb(*, pdbrc: PathLike | None = None) -> None:
    if pdbrc is not None:
        symlink(PDBRC, pdbrc)


def setup_psql(*, psqlrc: PathLike | None = None) -> None:
    if psqlrc is not None:
        symlink(PSQLRC, psqlrc)


def setup_resolv_conf(
    *, resolv_conf: PathLike | None = None, immutable: bool = False
) -> None:
    if resolv_conf is not None:
        cp(RESOLV_CONF, resolv_conf, immutable=immutable)


def setup_ssh(
    *,
    symlinks: Iterable[PathLike | tuple[PathLike, str]] = (),
    templates: Iterable[
        tuple[PathLike, Mapping[str, Any]] | tuple[PathLike, Mapping[str, Any], str]
    ] = (),
) -> None:
    write_text("Include config.d/*", SSH_CONFIG)
    mkdir(SSH_CONFIG_D, ownership=True)
    for sym in symlinks:
        match sym:
            case Path() | str() as path_to:
                name = full_path(path_to).name
            case Path() | str() as path_to, str() as name:
                ...
            case never:
                assert_never(never)
        if path_to is not None:
            symlink(SSH_CONFIG_D / name, path_to)
    for tem in templates:
        match tem:
            case Path() | str() as template, Mapping() as kwargs:
                name = full_path(template).name
            case Path() | str() as template, Mapping() as kwargs, str() as name:
                ...
            case never:
                assert_never(never)
        write_template(template, SSH_CONFIG_D / name, **kwargs)


def setup_ssh_keys(ssh_keys: PathLike, /) -> None:
    def run(path: PathLike, /) -> None:
        keys = [
            stripped
            for line in full_path(path).read_text().splitlines()
            if (stripped := line.strip()) != ""
        ]
        text = "\n".join(keys) + "\n"
        write_text(text, AUTHORIZED_KEYS)

    if isinstance(ssh_keys, Path) or full_path(ssh_keys).exists():
        run(ssh_keys)
        return
    with yield_download(ssh_keys) as temp_file:
        run(temp_file)


def setup_sshd(*, permit_root_login: bool = False) -> None:
    value = "prohibit-password" if permit_root_login else "no"
    replace_lines(
        "/etc/ssh/sshd_config",
        ("#PasswordAuthentication yes", "PasswordAuthentication no"),
        ("#PermitRootLogin prohibit-password", f"PermitRootLogin {value}"),
        ("#PubkeyAuthentication yes", "PubkeyAuthentication yes"),
    )


__all__ = [
    "add_to_known_hosts",
    "install_age",
    "install_agg",
    "install_asciinema",
    "install_bat",
    "install_brew",
    "install_build_essential",
    "install_bump_my_version",
    "install_curl",
    "install_delta",
    "install_direnv",
    "install_docker",
    "install_dropbox",
    "install_dust",
    "install_eza",
    "install_fd",
    "install_fish",
    "install_fzf",
    "install_ggrep",
    "install_gh",
    "install_ghostty",
    "install_git",
    "install_gitweb",
    "install_glab",
    "install_gsed",
    "install_iperf3",
    "install_jq",
    "install_just",
    "install_libpq",
    "install_luacheck",
    "install_luarocks",
    "install_maturin",
    "install_neovim",
    "install_neovim_dependencies",
    "install_postico",
    "install_pre_commit",
    "install_protonvpn",
    "install_pyright",
    "install_restic",
    "install_ripgrep",
    "install_rlwrap",
    "install_rsync",
    "install_ruff",
    "install_shellcheck",
    "install_shfmt",
    "install_sops",
    "install_spotify",
    "install_starship",
    "install_stylua",
    "install_syncthing",
    "install_tailscale",
    "install_taplo",
    "install_tmux",
    "install_topgrade",
    "install_transmission",
    "install_uv",
    "install_vim",
    "install_vlc",
    "install_vs_code",
    "install_watch",
    "install_watchexec",
    "install_wezterm",
    "install_whatsapp",
    "install_xclip",
    "install_yq",
    "install_zoom",
    "install_zoxide",
    "setup_bashrc",
    "setup_local_bin",
    "setup_pdb",
    "setup_psql",
    "setup_resolv_conf",
    "setup_ssh",
    "setup_ssh_keys",
    "setup_sshd",
]
