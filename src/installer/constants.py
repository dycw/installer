from __future__ import annotations

from collections.abc import Set as AbstractSet
from platform import machine, system
from re import IGNORECASE, search
from typing import TYPE_CHECKING

from utilities.iterables import OneEmptyError, one
from utilities.shellingham import get_shell
from utilities.subprocess import run
from utilities.typing import get_args

from installer.types import System

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable


SHELL = get_shell()


def _get_system_name() -> System:
    sys = system()
    systems: tuple[System, ...] = get_args(System)
    if sys in systems:
        return sys
    msg = f"Invalid system name; must be in {systems} but got {sys!r}"
    raise ValueError(msg)


SYSTEM_NAME = _get_system_name()


def _get_unique_group[T: AbstractSet[str]](
    groups: Iterable[T], predicate: Callable[[str], bool], /
) -> T:
    return one(g for g in groups if any(map(predicate, g)))


def _get_system_name_group() -> set[str]:
    groups: list[set[str]] = [{"darwin", "macos"}, {"linux"}]
    system_ = SYSTEM_NAME.lower()

    def predicate(text: str, /) -> bool:
        return text.lower() == system_

    try:
        return _get_unique_group(groups, predicate)
    except OneEmptyError:
        msg = f"Invalid system name; must be in {groups} but got {system_!r}"
        raise ValueError(msg) from None


SYSTEM_NAME_GROUP = _get_system_name_group()


def _get_c_std_lib_group() -> set[str] | None:
    try:
        result = run("ldd", "--version", return_=True)
    except FileNotFoundError:
        return None
    groups: list[set[str]] = [{"gnu", "glibc"}, {"musl"}]

    def predicate(text: str, /) -> bool:
        return search(text, result, flags=IGNORECASE) is not None

    try:
        return _get_unique_group(groups, predicate)
    except OneEmptyError:
        msg = f"Invalid C standard library; must be in {groups} but got {result!r}"
        raise ValueError(msg) from None


C_STD_LIB_GROUP = _get_c_std_lib_group()


def _get_machine_type_group() -> set[str]:
    groups: list[set[str]] = [
        {"amd64", "intel64", "x64", "x86_64"},
        {"aarch64", "arm64"},
    ]
    machine_ = machine().lower()

    def predicate(text: str, /) -> bool:
        return text.lower() == machine_

    try:
        return _get_unique_group(groups, predicate)
    except OneEmptyError:
        msg = f"Invalid machine type; must be in {groups} but got {machine_!r}"
        raise ValueError(msg) from None


MACHINE_TYPE_GROUP = _get_machine_type_group()


__all__ = [
    "C_STD_LIB_GROUP",
    "MACHINE_TYPE_GROUP",
    "SHELL",
    "SYSTEM_NAME",
    "SYSTEM_NAME_GROUP",
]
