from __future__ import annotations

from typing import assert_never

from typed_settings import Secret


def convert_token(x: str | None, /) -> Secret[str] | None:
    empty = {None, ""}
    match x:
        case Secret():
            match x.get_secret_value():
                case None:
                    return None
                case str():
                    return None if x.strip("\n") in empty else x.strip("\n")
                case never:
                    assert_never(never)
        case str():
            return None if x.strip("\n") in empty else Secret(x.strip("\n"))
        case None:
            return None
        case never:
            assert_never(never)
