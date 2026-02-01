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
            param(["apt-package", "git", "--ssh", "user@hostname"]),
            param(["apt-package", "git", "--sudo"]),
            param(["apt-package", "git", "--retry", "1", "1"]),
            param(["curl"], id="curl"),
            param(["curl", "--ssh", "user@hostname"]),
            param(["curl", "--sudo"]),
            param(["curl", "--retry", "1", "1"]),
            param(["git"], id="git"),
            param(["git", "--ssh", "user@hostname"]),
            param(["git", "--sudo"]),
            param(["git", "--retry", "1", "1"]),
            param(["jq"], id="jq"),
            param(["jq", "--force"]),
            param(["jq", "--path-binaries", "path"]),
            param(["jq", "--token", "token"]),
            param(["jq", "--sudo"]),
            param(["jq", "--perms", "perms"]),
            param(["jq", "--owner", "owner"]),
            param(["jq", "--group", "group"]),
            param(["ripgrep"], id="ripgrep"),
            param(["rsync"], id="rsync"),
            param(["rsync", "--ssh", "user@hostname"]),
            param(["rsync", "--sudo"]),
            param(["rsync", "--retry", "1", "1"]),
            param(["ruff"], id="ruff"),
            param(["sd"], id="sd"),
            param(["shellcheck"], id="shellcheck"),
            param(["shfmt"], id="shfmt"),
            param(["taplo"], id="taplo"),
            param(["uv"], id="uv"),
            param(["uv", "--ssh", "user@hostname"]),
            param(["uv", "--token", "token"]),
            param(["uv", "--path-binaries", "path"]),
            param(["uv", "--sudo"]),
            param(["uv", "--perms", "perms"]),
            param(["uv", "--owner", "owner"]),
            param(["uv", "--group", "group"]),
            param(["uv", "--retry", "1", "1"]),
            param(["yq"], id="yq"),
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

    @mark.parametrize(
        "args",
        [
            param([]),
            param(["--sudo"]),
            param(["--user", "user"]),
            param(["--ssh", "user@hostname"]),
            param(["--force"]),
            param(["--retry", "1", "1"]),
        ],
    )
    @throttle_test(duration=MINUTE)
    def test_commands_docker(self, *, args: list[str]) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["docker", *args])
        assert result.exit_code == 0, result.stderr

    @mark.parametrize(
        "cmd",
        [
            param("age"),
            param("bat"),
            param("btm"),
            param("delta"),
            param("dust"),
            param("eza"),
            param("fd"),
            param("just"),
            param("nvim"),
            param("restic"),
            param("sops"),
        ],
    )
    @mark.parametrize(
        "args",
        [
            param([]),
            param(["--token", "token"]),
            param(["--path-binaries", "path"]),
            param(["--sudo"]),
            param(["--perms", "perms"]),
            param(["--owner", "owner"]),
            param(["--group", "group"]),
            param(["--ssh", "user@hostname"]),
            param(["--force"]),
            param(["--retry", "1", "1"]),
        ],
    )
    @throttle_test(duration=MINUTE)
    def test_commands_github(self, *, cmd: str, args: list[str]) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, [cmd, *args])
        assert result.exit_code == 0, result.stderr

    @mark.parametrize(
        "cmd", [param("direnv"), param("fzf"), param("starship"), param("zoxide")]
    )
    @mark.parametrize(
        "args",
        [
            param([]),
            param(["--token", "token"]),
            param(["--path-binaries", "path"]),
            param(["--sudo"]),
            param(["--perms-binary", "perms"]),
            param(["--owner", "owner"]),
            param(["--group", "group"]),
            param(["--etc"]),
            param(["--shell", "bash"]),
            param(["--home", "path"]),
            param(["--perms-config", "perms"]),
            param(["--root", "path"]),
            param(["--ssh", "user@hostname"]),
            param(["--force"]),
            param(["--retry", "1", "1"]),
        ],
    )
    @throttle_test(duration=MINUTE)
    def test_commands_github_with_shell(self, *, cmd: str, args: list[str]) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, [cmd, *args])
        assert result.exit_code == 0, result.stderr

    @throttle_test(duration=MINUTE)
    def test_commands_starship(self) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["starship", "--starship-toml", "path"])
        assert result.exit_code == 0, result.stderr

    @mark.parametrize(
        "args",
        [
            param([]),
            param(["--token", "token"]),
            param(["--ssh", "user@hostname"]),
            param(["--force"]),
            param(["--retry", "1", "1"]),
        ],
    )
    @throttle_test(duration=MINUTE)
    def test_commands_pve_fake_subscription(self, *, args: list[str]) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["pve-fake-subscription", *args])
        assert result.exit_code == 0, result.stderr

    @mark.parametrize(
        "args",
        [
            param([]),
            param(["--host", "host"]),
            param(["--retry", "1", "1"]),
            param(["--port", "1234"]),
            param(["--dest", "dest"]),
            param(["--branch", "branch"]),
        ],
    )
    @throttle_test(duration=MINUTE)
    def test_git_clone(self, *, tmp_path: Path, args: list[str]) -> None:
        key = tmp_path / "key.txt"
        key.touch()
        runner = CliRunner()
        result = runner.invoke(cli, ["git-clone", str(key), "owner", "repo", *args])
        assert result.exit_code == 0, result.stderr

    @throttle_test(duration=MINUTE)
    def test_entrypoint(self) -> None:
        run("cli", "--help")

    @skipif_ci
    @throttle_test(duration=MINUTE)
    def test_justfile(self) -> None:
        run("just", "cli", "--help")
