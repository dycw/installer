from __future__ import annotations

from click import command, echo
from click.testing import CliRunner
from pytest import MonkeyPatch, mark, param
from typed_settings import Secret, click_options, secret, settings

from github_downloader.settings import LOADER
from github_downloader.utilities import convert_token


@settings
class _SettingsWithSecret:
    token: Secret[str] | None = secret(default=None, converter=convert_token)


@command()
@click_options(_SettingsWithSecret, [LOADER], show_envvars_in_help=True)
def _cli_with_token(settings: _SettingsWithSecret, /) -> None:
    if (value := settings.token) is None:
        echo("token = None")
    else:
        echo(f"token = {value.get_secret_value()}")


class TestConvertToken:
    def test_missing(self) -> None:
        result = CliRunner().invoke(_cli_with_token)
        assert result.exit_code == 0
        assert result.stdout == "token = None\n"

    @mark.parametrize("value", [param("value"), param("value\n"), param("\nvalue")])
    def test_cli(self, *, value: str) -> None:
        result = CliRunner().invoke(_cli_with_token, args=["--token", value])
        assert result.exit_code == 0
        assert result.stdout == "token = value\n"

    @mark.parametrize(
        ("value", "expected"),
        [
            param("value", "value"),
            param("value\n", "value"),
            param("\nvalue", "value"),
            param("", "None"),
        ],
    )
    def test_env(self, *, monkeypatch: MonkeyPatch, value: str, expected: str) -> None:
        monkeypatch.setenv("TOKEN", value)

        @command()
        @click_options(_SettingsWithSecret, [LOADER], show_envvars_in_help=True)
        def _cli_with_secret(settings: _SettingsWithSecret, /) -> None:
            if (value := settings.token) is None:
                echo("token = None")
            else:
                echo(f"token = {value.get_secret_value()}")

        result = CliRunner().invoke(_cli_with_secret)
        assert result.exit_code == 0
        assert result.stdout == f"token = {expected}\n"
