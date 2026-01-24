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
            param(["apt-package", "git"], id="apt-package"),
            param(["age"], id="age"),
            param(["bat"], id="bat"),
            param(["btm"], id="btm"),
            param(["curl"], id="curl"),
            param(["delta"], id="delta"),
            param(["direnv"], id="direnv"),
            param(["docker"], id="docker"),
            param(["dust"], id="dust"),
            param(["eza"], id="eza"),
            param(["fd"], id="fd"),
            param(["fzf"], id="fzf"),
            param(["git"], id="git"),
            param(["jq"], id="jq"),
            param(["just"], id="just"),
            param(["neovim"], id="neovim"),
            param(["restic"], id="restic"),
            param(["ripgrep"], id="ripgrep"),
            param(["rsync"], id="rsync"),
            param(["ruff"], id="ruff"),
            param(["sd"], id="sd"),
            param(["shellcheck"], id="shellcheck"),
            param(["shfmt"], id="shfmt"),
            param(["sops"], id="sops"),
            param(["starship"], id="starship"),
            param(["taplo"], id="taplo"),
            param(["uv"], id="uv"),
            param(["yq"], id="yq"),
            param(["zoxide"], id="zoxide"),
            ##
            param(["setup-authorized-keys"], id="setup-authorized-keys 0"),
            param(["setup-authorized-keys", "key1"], id="setup-authorized-keys 1"),
            param(
                ["setup-authorized-keys", "key1", "key2"], id="setup-authorized-keys 2"
            ),
            param(["setup-ssh-config"], id="setup-ssh-config"),
            param(["setup-sshd-config"], id="setup-sshd-config"),
            ##
            param(["--version"], id="version"),
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
