from __future__ import annotations

from os import environ

from pytest import fixture
from typed_settings import Secret
from utilities.hypothesis import setup_hypothesis_profiles

setup_hypothesis_profiles()


@fixture
def token() -> Secret[str] | None:
    try:
        return Secret(environ["GITHUB_TOKEN"])
    except KeyError:
        return None
