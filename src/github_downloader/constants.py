from __future__ import annotations

from collections.abc import Set as AbstractSet
from platform import machine, system
from re import IGNORECASE, search
from typing import TYPE_CHECKING, Any, cast

from utilities.iterables import OneEmptyError, one
from utilities.subprocess import run

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from github_downloader.types import System


def _get_system_name() -> System:
    sys = system()
    names = {"Darwin", "Linux"}
    if sys in names:
        return cast("Any", sys)
    msg = f"Invalid system name; must be in {names} but got {sys!r}"
    raise ValueError(msg)


SYSTEM_NAME = _get_system_name()


def _get_unique_group[T: AbstractSet[str]](
    groups: Iterable[T], predicate: Callable[[str], bool], /
) -> T:
    return one(g for g in groups if any(map(predicate, g)))


def _get_c_std_lib_group(system: System, /) -> set[str] | None:
    if system == "Darwin":
        return None
    groups: list[set[str]] = [{"gnu", "glibc"}, {"musl"}]
    result = run("ldd", "--version", return_=True)

    def predicate(text: str, /) -> bool:
        return search(text, result, flags=IGNORECASE) is not None

    try:
        return _get_unique_group(groups, predicate)
    except OneEmptyError:
        msg = f"Invalid C standard library; must be in {groups} but got {result!r}"
        raise ValueError(msg) from None


C_STD_LIB_GROUP = _get_c_std_lib_group(SYSTEM_NAME)


MACHINE_TYPE = machine()


def _get_machine_type_group() -> set[str]:
    groups: list[set[str]] = [
        {"amd64", "intel64", "x64", "x86_64"},
        {"aarch64", "arm64"},
    ]

    def predicate(text: str, /) -> bool:
        return text == MACHINE_TYPE

    try:
        return _get_unique_group(groups, predicate)
    except OneEmptyError:
        msg = f"Invalid machine type; must be in {groups} but got {MACHINE_TYPE!r}"
        raise ValueError(msg) from None


MACHINE_TYPE_GROUP = _get_machine_type_group()

__all__ = ["C_STD_LIB_GROUP", "MACHINE_TYPE", "MACHINE_TYPE_GROUP", "SYSTEM_NAME"]
