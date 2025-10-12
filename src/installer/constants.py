from __future__ import annotations

from pathlib import Path

HOME = Path("~").expanduser()
XDG_CONFIG_HOME = HOME / ".config"
LOCAL_BIN = HOME / ".local/bin"
SSH = HOME / ".ssh"


INSTALL = Path(__file__).parent
REPO_ROOT = INSTALL.parent
BOTTOM_TOML = REPO_ROOT / "bottom/bottom.toml"
FD_IGNORE = REPO_ROOT / "fd/ignore"
_fish = REPO_ROOT / "fish"
FISH_CONFIG = _fish / "config.fish"
FISH_ENV = _fish / "env.fish"
FISH_GIT = _fish / "git.fish"
FISH_WORK = _fish / "work.fish"
FZF_FISH = REPO_ROOT / "fzf/fzf.fish"
_git = REPO_ROOT / "git"
GIT_CONFIG = _git / "config"
GIT_IGNORE = _git / "ignore"
NVIM = REPO_ROOT / "nvim"
PDBRC = REPO_ROOT / "pdb/pdbrc"
PSQLRC = REPO_ROOT / "psql/psqlrc"
RIPGREPRC = REPO_ROOT / "ripgrep/ripgreprc"
SSH_CONFIG = REPO_ROOT / "ssh/config"
STARSHIP_TOML = REPO_ROOT / "starship/starship.toml"
_tmux = REPO_ROOT / "tmux"
TMUX_CONF_OH_MY_TMUX = _tmux / ".tmux/.tmux.conf"
TMUX_CONF_LOCAL = _tmux / "tmux.conf.local"
WEZTERM_LUA = XDG_CONFIG_HOME / "wezterm/wezterm.lua"


__all__ = [
    "BOTTOM_TOML",
    "FD_IGNORE",
    "FISH_CONFIG",
    "FISH_ENV",
    "FISH_GIT",
    "FISH_WORK",
    "FZF_FISH",
    "GIT_CONFIG",
    "GIT_IGNORE",
    "HOME",
    "INSTALL",
    "LOCAL_BIN",
    "NVIM",
    "PDBRC",
    "PSQLRC",
    "REPO_ROOT",
    "RIPGREPRC",
    "SSH",
    "SSH_CONFIG",
    "STARSHIP_TOML",
    "TMUX_CONF_LOCAL",
    "TMUX_CONF_OH_MY_TMUX",
    "WEZTERM_LUA",
    "XDG_CONFIG_HOME",
]
