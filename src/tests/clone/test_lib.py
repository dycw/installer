from __future__ import annotations

from re import search
from typing import TYPE_CHECKING

from utilities.core import normalize_multi_line_str

from installer.clone.lib import _setup_deploy_key

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
