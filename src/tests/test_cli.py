from __future__ import annotations

from pytest import mark, param
from utilities.subprocess import run


class TestCLI:
    @mark.parametrize(
        "args",
        [
            param(["age"]),
            param(["direnv"]),
            param(["run", "asset-owner", "asset-repo", "binary-name"]),
            param(["ripgrep"]),
            param(["sops"]),
            param(["starship"]),
        ],
    )
    def test_main(self, *, args: list[str]) -> None:
        run("github-download", *args)
