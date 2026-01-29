from __future__ import annotations

from re import search
from typing import TYPE_CHECKING

from utilities.constants import MINUTE
from utilities.core import normalize_multi_line_str
from utilities.pytest import throttle_test

from installer.clone.lib import (
    _set_up_deploy_key,
    _set_up_known_hosts,
    _set_up_ssh_conf,
)

if TYPE_CHECKING:
    from pathlib import Path


class TestSetUpDeployKey:
    def test_main(self, *, tmp_path: Path) -> None:
        src = tmp_path / "key"
        _ = src.write_text("key")
        _set_up_deploy_key(src, home=tmp_path)
        path = tmp_path / ".ssh/deploy-keys/key"
        assert path.is_file()
        assert path.read_text() == "key"


class TestSetUpKnownHosts:
    @throttle_test(duration=5 * MINUTE)
    def test_main(self, *, tmp_path: Path) -> None:
        _set_up_known_hosts(home=tmp_path)
        path = tmp_path / ".ssh/known_hosts"
        assert path.is_file()
        assert search(r"^github.com ssh-ed25519 \w+$", path.read_text())


class TestSetUpSSHConf:
    def test_main(self, *, tmp_path: Path) -> None:
        src = tmp_path / "key"
        _ = src.write_text("key")
        _set_up_ssh_conf(src, home=tmp_path)
        path = tmp_path / ".ssh/config.d/key.conf"
        assert path.is_file()
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
        assert search(pattern, path.read_text())
