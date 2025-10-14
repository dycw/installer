from __future__ import annotations

from pathlib import Path

HOME = Path("~").expanduser()


BASHRC = HOME / ".bashrc"
LOCAL_BIN = HOME / ".local/bin"
PDBRC = HOME / ".pdbrc"
PSQLRC = HOME / ".psqlrc"
SSH = HOME / ".ssh"
XDG_CONFIG_HOME = HOME / ".config"


AUTHORIZED_KEYS = SSH / "authorized_keys"
KNOWN_HOSTS = SSH / "known_hosts"
SSH_CONFIG = SSH / "config"


CONFIG_BOTTOM_TOML = XDG_CONFIG_HOME / "bottom/bottom.toml"
CONFIG_DIRENV = XDG_CONFIG_HOME / "direnv"
CONFIG_FD_IGNORE = XDG_CONFIG_HOME / "fd/ignore"
CONFIG_FISH = XDG_CONFIG_HOME / "fish"
CONFIG_FISH_CONF_D = CONFIG_FISH / "conf.d"
CONFIG_FISH_FUNCTIONS = CONFIG_FISH / "functions"
CONFIG_GIT = XDG_CONFIG_HOME / "git"
CONFIG_GLAB_CONFIG_YML = XDG_CONFIG_HOME / "glab-cli/config.yml"
CONFIG_NVIM = XDG_CONFIG_HOME / "nvim"
CONFIG_SOPS_AGE = XDG_CONFIG_HOME / "sops/age/keys.txt"
CONFIG_STARSHIP_TOML = XDG_CONFIG_HOME / "starship.toml"
CONFIG_TMUX = XDG_CONFIG_HOME / "tmux"
CONFIG_TMUX_CONF_OH_MY_TMUX = CONFIG_TMUX / "tmux.conf"
CONFIG_TMUX_CONF_LOCAL = CONFIG_TMUX / "tmux.conf.local"
CONFIG_WEZTERM_LUA = XDG_CONFIG_HOME / "wezterm/wezterm.lua"


__all__ = [
    "AUTHORIZED_KEYS",
    "BASHRC",
    "CONFIG_BOTTOM_TOML",
    "CONFIG_DIRENV",
    "CONFIG_FD_IGNORE",
    "CONFIG_FISH",
    "CONFIG_FISH_CONF_D",
    "CONFIG_FISH_FUNCTIONS",
    "CONFIG_GIT",
    "CONFIG_GLAB_CONFIG_YML",
    "CONFIG_NVIM",
    "CONFIG_SOPS_AGE",
    "CONFIG_STARSHIP_TOML",
    "CONFIG_TMUX",
    "CONFIG_TMUX_CONF_LOCAL",
    "CONFIG_TMUX_CONF_OH_MY_TMUX",
    "CONFIG_WEZTERM_LUA",
    "HOME",
    "KNOWN_HOSTS",
    "LOCAL_BIN",
    "PDBRC",
    "PSQLRC",
    "SSH",
    "SSH_CONFIG",
    "XDG_CONFIG_HOME",
]
