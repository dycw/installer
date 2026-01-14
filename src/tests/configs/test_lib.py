from __future__ import annotations

from typing import TYPE_CHECKING

from installer.configs.lib import (
    setup_authorized_keys,
    setup_ssh_config,
    setup_sshd_config,
)

if TYPE_CHECKING:
    from pathlib import Path


class TestSetupAuthorizedKeys:
    def test_main(self, *, tmp_path: Path) -> None:
        setup_authorized_keys([], root=tmp_path)


class TestSetupSSHConfig:
    def test_main(self, *, tmp_path: Path) -> None:
        setup_ssh_config(root=tmp_path)


class TestSetupSSHDConfig:
    def test_main(self, *, tmp_path: Path) -> None:
        setup_sshd_config(root=tmp_path)
