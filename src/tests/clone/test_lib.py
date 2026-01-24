from __future__ import annotations

from typing import TYPE_CHECKING

from installer.clone.lib import _setup_deploy_key

if TYPE_CHECKING:
    from pathlib import Path


class TestSetupDeployKey:
    def test_main(self, *, tmp_path: Path) -> None:
        path = tmp_path / "key.txt"
        path.touch()
        _setup_deploy_key(path, home=tmp_path)
