from __future__ import annotations

from os import environ
from typing import TYPE_CHECKING

from pytest import fixture
from typed_settings import Secret
from utilities.constants import HOUR
from utilities.hypothesis import setup_hypothesis_profiles

if TYPE_CHECKING:
    from utilities.types import Duration

setup_hypothesis_profiles()


RUN_TEST_FRAC: float = 0.1
THROTTLE_DURATION: Duration = HOUR


@fixture
def token() -> Secret[str] | None:
    try:
        return Secret(environ["GITHUB_TOKEN"])
    except KeyError:
        return None
