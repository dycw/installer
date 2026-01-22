from __future__ import annotations

from typing import TYPE_CHECKING

from click.testing import CliRunner
from pytest import mark, param
from utilities.pytest import skipif_ci
from utilities.subprocess import run

from installer.cli import cli

if TYPE_CHECKING:
    from pathlib import Path


class TestCLI:
    @mark.parametrize(
        "commands",
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
    def test_commands(self, *, commands: list[str]) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, commands)
        assert result.exit_code == 0, result.stderr

    def test_git_clone(self, *, tmp_path: Path) -> None:
        key = tmp_path / "key.txt"
        key.touch()
        runner = CliRunner()
        result = runner.invoke(cli, ["git-clone", str(key), "owner", "repo"])
        assert result.exit_code == 0, result.stderr

    def test_entrypoint(self) -> None:
        run("cli", "--help")

    @skipif_ci
    def test_justfile(self) -> None:
        run("just", "cli", "--help")
