from __future__ import annotations

from typing import TYPE_CHECKING

from pytest import mark, param
from utilities.subprocess import run

if TYPE_CHECKING:
    from pathlib import Path


class TestCLI:
    @mark.parametrize(
        "args",
        [
            ##
            param(["age"]),
            param(["bat"]),
            param(["btm"]),
            param(["curl"]),
            param(["delta"]),
            param(["direnv"]),
            param(["dust"]),
            param(["eza"]),
            param(["fd"]),
            param(["fzf"]),
            param(["git"]),
            param(["jq"]),
            param(["just"]),
            param(["neovim"]),
            param(["restic"]),
            param(["ripgrep"]),
            param(["rsync"]),
            param(["ruff"]),
            param(["sd"]),
            param(["shellcheck"]),
            param(["shfmt"]),
            param(["sops"]),
            param(["starship"]),
            param(["taplo"]),
            param(["uv"]),
            param(["yq"]),
            param(["zoxide"]),
            ##
            param(["setup-authorized-keys"]),
            param(["setup-authorized-keys", "key1"]),
            param(["setup-authorized-keys", "key1", "key2"]),
            param(["setup-ssh-config"]),
            param(["setup-sshd-config"]),
        ],
    )
    def test_main(self, *, args: list[str]) -> None:
        run("cli", *args)

    def test_git_clone(self, *, tmp_path: Path) -> None:
        key = tmp_path / "key.txt"
        key.touch()
        run("cli", "git-clone", str(key), "owner", "repo", cwd=tmp_path)
