from __future__ import annotations

from re import search
from typing import TYPE_CHECKING

from utilities.constants import MINUTE
from utilities.core import normalize_multi_line_str
from utilities.pytest import throttle_test

from installer.clone.lib import _setup_deploy_key, _setup_known_hosts

if TYPE_CHECKING:
    from pathlib import Path


class TestSetupDeployKey:
    def test_main(self, *, tmp_path: Path) -> None:
        src = tmp_path / "key"
        _ = src.write_text("key")
        _setup_deploy_key(src, home=tmp_path)
        config = tmp_path / ".ssh/config.d/key.conf"
        assert config.is_file()
        pattern = normalize_multi_line_str(f"""
            Host key
                User git
                HostName github.com
                IdentityFile {tmp_path}/.ssh/deploy-keys/key
                IdentitiesOnly yes
                BatchMode yes
                HostKeyAlgorithms ssh-ed25519
                StrictHostKeyChecking yes
        """)
        assert search(pattern, config.read_text())
        key = tmp_path / ".ssh/deploy-keys/key"
        assert key.is_file()
        assert key.read_text() == "key"


class TestSetupKnownHosts:
    @throttle_test(duration=5 * MINUTE)
    def test_main(self, *, tmp_path: Path) -> None:
        _setup_known_hosts(home=tmp_path)
        path = tmp_path / ".ssh/known_hosts"
        assert path.is_file()
        assert search(r"^github.com ssh-ed25519 \w+$", path.read_text())
