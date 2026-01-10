from __future__ import annotations

from typing import Literal

type Shell = Literal["bash", "fish", "zsh"]
type System = Literal["Darwin", "Linux"]


__all__ = ["Shell", "System"]
