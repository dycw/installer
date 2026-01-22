from __future__ import annotations

from typing import TYPE_CHECKING

from utilities.text import normalize_multi_line_str

from installer.configs.lib import (
    setup_authorized_keys,
    setup_ssh_config,
    setup_sshd_config,
    sshd_config,
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


class TestSSHDConfig:
    def test_main(self) -> None:
        result = sshd_config()
        expected = normalize_multi_line_str("""
            PasswordAuthentication no
            PermitRootLogin no
            PubkeyAcceptedAlgorithms ssh-ed25519
            PubkeyAuthentication yes
        """)
        assert result == expected
