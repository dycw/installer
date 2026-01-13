from __future__ import annotations

from pytest import mark, param
from utilities.subprocess import run


class TestCLI:
    @mark.parametrize(
        "args",
        [
            param(["age"]),
            param(["btm"]),
            param(["direnv"]),
            param(["fd"]),
            param(["fzf"]),
            param(["git"]),
            param(["jq"]),
            param(["just"]),
            param(["restic"]),
            param(["ripgrep"]),
            param(["rsync"]),
            param(["run", "asset-owner", "asset-repo", "binary-name"]),
            param(["sd"]),
            param(["shellcheck"]),
            param(["shfmt"]),
            param(["sops"]),
            param(["starship"]),
            param(["yq"]),
        ],
    )
    def test_main(self, *, args: list[str]) -> None:
        run("installer", *args)
