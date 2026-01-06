from __future__ import annotations

from re import search
from typing import TYPE_CHECKING

from utilities.pytest import throttle
from utilities.subprocess import run
from utilities.whenever import MINUTE

from github_downloader.lib import setup_sops

if TYPE_CHECKING:
    from pathlib import Path

    from pytest import CaptureFixture
    from typed_settings import Secret


class TestSetupSops:
    @throttle(delta=5 * MINUTE)
    def test_main(
        self, *, token: Secret[str] | None, tmp_path: Path, capsys: CaptureFixture
    ) -> None:
        setup_sops(token=token, path_binaries=tmp_path)
        run(str(tmp_path / "sops"), "--help", print=True)
        out = capsys.readouterr().out
        expected = "sops - sops - encrypted file editor with AWS KMS, GCP KMS, Azure Key Vault, age, and GPG"
        assert search(expected, out)
