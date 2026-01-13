from __future__ import annotations

from pytest import mark, param
from utilities.subprocess import run


class TestCLI:
    @mark.parametrize(
        "args",
        [
            param(["age"]),
            param(["btm"]),
            param(["delta"]),
            param(["direnv"]),
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
            param(["run", "asset-owner", "asset-repo", "binary-name"]),
            param(["sd"]),
            param(["shellcheck"]),
            param(["shfmt"]),
            param(["sops"]),
            param(["starship"]),
            param(["taplo"]),
            param(["uv"]),
            param(["yq"]),
            param(["zoxide"]),
        ],
    )
    def test_main(self, *, args: list[str]) -> None:
        run("installer", *args)
