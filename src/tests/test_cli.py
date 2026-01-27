from __future__ import annotations

from typing import TYPE_CHECKING

from click.testing import CliRunner
from pytest import mark, param
from utilities.constants import MINUTE
from utilities.pytest import skipif_ci, throttle_test
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
            param(["age", "--logger", "logger"]),
            param(["age", "--ssh", "user@hostname"]),
            param(["age", "--token", "token"]),
            param(["age", "--path-binaries", "path"]),
            param(["age", "--sudo"]),
            param(["age", "--perms", "perms"]),
            param(["age", "--owner", "owner"]),
            param(["age", "--group", "group"]),
            param(["age", "--retry", "1", "1"]),
            param(["bat"], id="bat"),
            param(["btm"], id="btm"),
            param(["curl"], id="curl"),
            param(["curl", "--logger", "logger"]),
            param(["curl", "--ssh", "user@hostname"]),
            param(["curl", "--sudo"]),
            param(["curl", "--retry", "1", "1"]),
            param(["delta"], id="delta"),
            param(["direnv"], id="direnv"),
            param(["direnv", "--logger", "logger"]),
            param(["direnv", "--ssh", "user@hostname"]),
            param(["direnv", "--path-binaries", "path"]),
            param(["direnv", "--token", "token"]),
            param(["direnv", "--sudo"]),
            param(["direnv", "--perms-binary", "perms"]),
            param(["direnv", "--owner", "owner"]),
            param(["direnv", "--group", "group"]),
            param(["direnv", "--etc"]),
            param(["direnv", "--home", "home"]),
            param(["direnv", "--perms-config", "perms"]),
            param(["direnv", "--retry", "1", "1"]),
            param(["docker"], id="docker"),
            param(["docker", "--logger", "logger"]),
            param(["docker", "--ssh", "user@hostname"]),
            param(["docker", "--sudo"]),
            param(["docker", "--user", "user"]),
            param(["docker", "--retry", "1", "1"]),
            param(["dust"], id="dust"),
            param(["eza"], id="eza"),
            param(["fd"], id="fd"),
            param(["fzf"], id="fzf"),
            param(["fzf", "--logger", "logger"]),
            param(["fzf", "--ssh", "user@hostname"]),
            param(["fzf", "--token", "token"]),
            param(["fzf", "--path-binaries", "path"]),
            param(["fzf", "--sudo"]),
            param(["fzf", "--perms-binary", "perms"]),
            param(["fzf", "--owner", "owner"]),
            param(["fzf", "--group", "group"]),
            param(["fzf", "--etc"]),
            param(["fzf", "--home", "home"]),
            param(["fzf", "--perms-config", "perms"]),
            param(["fzf", "--retry", "1", "1"]),
            param(["git"], id="git"),
            param(["git", "--logger", "logger"]),
            param(["git", "--ssh", "user@hostname"]),
            param(["git", "--sudo"]),
            param(["git", "--retry", "1", "1"]),
            param(["jq"], id="jq"),
            param(["just"], id="just"),
            param(["just", "--logger", "logger"]),
            param(["just", "--ssh", "user@hostname"]),
            param(["just", "--token", "token"]),
            param(["just", "--path-binaries", "path"]),
            param(["just", "--sudo"]),
            param(["just", "--perms", "perms"]),
            param(["just", "--owner", "owner"]),
            param(["just", "--group", "group"]),
            param(["just", "--retry", "1", "1"]),
            param(["neovim"], id="neovim"),
            param(["restic"], id="restic"),
            param(["restic", "--logger", "logger"]),
            param(["restic", "--ssh", "user@hostname"]),
            param(["restic", "--token", "token"]),
            param(["restic", "--path-binaries", "path"]),
            param(["restic", "--sudo"]),
            param(["restic", "--perms", "perms"]),
            param(["restic", "--owner", "owner"]),
            param(["restic", "--group", "group"]),
            param(["restic", "--retry", "1", "1"]),
            param(["ripgrep"], id="ripgrep"),
            param(["rsync"], id="rsync"),
            param(["rsync", "--logger", "logger"]),
            param(["rsync", "--ssh", "user@hostname"]),
            param(["rsync", "--sudo"]),
            param(["rsync", "--retry", "1", "1"]),
            param(["ruff"], id="ruff"),
            param(["sd"], id="sd"),
            param(["shellcheck"], id="shellcheck"),
            param(["shfmt"], id="shfmt"),
            param(["sops"], id="sops"),
            param(["sops", "--logger", "logger"]),
            param(["sops", "--ssh", "user@hostname"]),
            param(["sops", "--token", "token"]),
            param(["sops", "--path-binaries", "path"]),
            param(["sops", "--sudo"]),
            param(["sops", "--perms", "perms"]),
            param(["sops", "--owner", "owner"]),
            param(["sops", "--group", "group"]),
            param(["sops", "--retry", "1", "1"]),
            param(["starship"], id="starship"),
            param(["starship", "--logger", "logger"]),
            param(["starship", "--ssh", "user@hostname"]),
            param(["starship", "--token", "token"]),
            param(["starship", "--path-binaries", "path"]),
            param(["starship", "--sudo"]),
            param(["starship", "--perms-binary", "perms"]),
            param(["starship", "--owner", "owner"]),
            param(["starship", "--group", "group"]),
            param(["starship", "--etc"]),
            param(["starship", "--home", "home"]),
            param(["starship", "--starship-toml", "starship.toml"]),
            param(["starship", "--perms-config", "perms"]),
            param(["starship", "--retry", "1", "1"]),
            param(["taplo"], id="taplo"),
            param(["uv"], id="uv"),
            param(["uv", "--logger", "logger"]),
            param(["uv", "--ssh", "user@hostname"]),
            param(["uv", "--token", "token"]),
            param(["uv", "--path-binaries", "path"]),
            param(["uv", "--sudo"]),
            param(["uv", "--perms", "perms"]),
            param(["uv", "--owner", "owner"]),
            param(["uv", "--group", "group"]),
            param(["uv", "--retry", "1", "1"]),
            param(["yq"], id="yq"),
            param(["zoxide"], id="zoxide"),
            param(["zoxide", "--logger", "logger"]),
            param(["zoxide", "--ssh", "user@hostname"]),
            param(["zoxide", "--token", "token"]),
            param(["zoxide", "--path-binaries", "path"]),
            param(["zoxide", "--sudo"]),
            param(["zoxide", "--perms-binary", "perms"]),
            param(["zoxide", "--owner", "owner"]),
            param(["zoxide", "--group", "group"]),
            param(["zoxide", "--etc"]),
            param(["zoxide", "--home", "home"]),
            param(["zoxide", "--perms-config", "perms"]),
            param(["zoxide", "--retry", "1", "1"]),
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
    @throttle_test(duration=MINUTE)
    def test_commands(self, *, commands: list[str]) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, commands)
        assert result.exit_code == 0, result.stderr

    @throttle_test(duration=MINUTE)
    def test_git_clone(self, *, tmp_path: Path) -> None:
        key = tmp_path / "key.txt"
        key.touch()
        runner = CliRunner()
        result = runner.invoke(cli, ["git-clone", str(key), "owner", "repo"])
        assert result.exit_code == 0, result.stderr

    @throttle_test(duration=MINUTE)
    def test_entrypoint(self) -> None:
        run("cli", "--help")

    @skipif_ci
    @throttle_test(duration=MINUTE)
    def test_justfile(self) -> None:
        run("just", "cli", "--help")
