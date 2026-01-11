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
            param(["fzf"]),
            param(["git"]),
            param(["just"]),
            param(["restic"]),
            param(["ripgrep"]),
            param(["run", "asset-owner", "asset-repo", "binary-name"]),
            param(["sops"]),
            param(["starship"]),
        ],
    )
    def test_main(self, *, args: list[str]) -> None:
        run("github-download", *args)
