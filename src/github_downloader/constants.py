from __future__ import annotations

from platform import machine, system

SYSTEM_NAME = system()
MACHINE_TYPE = machine()


__all__ = ["MACHINE_TYPE", "SYSTEM_NAME"]
