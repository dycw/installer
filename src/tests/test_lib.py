from __future__ import annotations

from re import escape, search
from typing import TYPE_CHECKING

from utilities.pytest import throttle_test
from utilities.subprocess import run
from utilities.text import strip_and_dedent
from utilities.whenever import MINUTE

from github_downloader.lib import setup_age, setup_ripgrep, setup_sops

if TYPE_CHECKING:
    from pathlib import Path

    from pytest import CaptureFixture
    from typed_settings import Secret


class TestSetupAge:
    @throttle_test(delta=5 * MINUTE)
    def test_main(
        self, *, token: Secret[str] | None, tmp_path: Path, capsys: CaptureFixture
    ) -> None:
        setup_age(token=token, path_binaries=tmp_path)

        run(str(tmp_path / "age"), "--help", print=True)
        result1 = capsys.readouterr()
        pattern1 = strip_and_dedent("""
            Usage:
                age [--encrypt] (-r RECIPIENT | -R PATH)... [--armor] [-o OUTPUT] [INPUT]
                age [--encrypt] --passphrase [--armor] [-o OUTPUT] [INPUT]
                age --decrypt [-i PATH]... [-o OUTPUT] [INPUT]
        """)
        assert search(escape(pattern1), result1.err)

        run(str(tmp_path / "age-inspect"), "--help", print=True)
        result2 = capsys.readouterr()
        pattern2 = strip_and_dedent("""
            Usage:
                age-inspect [--json] [INPUT]
        """)
        assert search(escape(pattern2), result2.err)

        run(str(tmp_path / "age-keygen"), "--help", print=True)
        result3 = capsys.readouterr()
        pattern3 = strip_and_dedent("""
            Usage:
                age-keygen [-pq] [-o OUTPUT]
                age-keygen -y [-o OUTPUT] [INPUT]
        """)
        assert search(escape(pattern3), result3.err)

        run(str(tmp_path / "age-plugin-batchpass"), "--help", print=True)
        result4 = capsys.readouterr()
        pattern4 = strip_and_dedent("""
            age-plugin-batchpass is an age plugin that enables non-interactive
            passphrase-based encryption and decryption using environment variables.
        """)
        assert search(escape(pattern4), result4.err)


class TestSetupRipgrep:
    @throttle_test(delta=5 * MINUTE)
    def test_main(
        self, *, token: Secret[str] | None, tmp_path: Path, capsys: CaptureFixture
    ) -> None:
        setup_ripgrep(token=token, path_binaries=tmp_path)
        run(str(tmp_path / "rg"), "--help", print=True)
        result = capsys.readouterr()
        pattern = strip_and_dedent("""
            USAGE:
                rg [OPTIONS] PATTERN [PATH ...]
                rg [OPTIONS] -e PATTERN ... [PATH ...]
                rg [OPTIONS] -f PATTERNFILE ... [PATH ...]
                rg [OPTIONS] --files [PATH ...]
                rg [OPTIONS] --type-list
                command | rg [OPTIONS] PATTERN
                rg [OPTIONS] --help
                rg [OPTIONS] --version
        """)
        assert search(escape(pattern), result.out)


class TestSetupSops:
    @throttle_test(delta=5 * MINUTE)
    def test_main(
        self, *, token: Secret[str] | None, tmp_path: Path, capsys: CaptureFixture
    ) -> None:
        setup_sops(token=token, path_binaries=tmp_path)
        run(str(tmp_path / "sops"), "--help", print=True)
        result = capsys.readouterr()
        pattern = strip_and_dedent("""
            NAME:
               sops - sops - encrypted file editor with AWS KMS, GCP KMS, Azure Key Vault, age, and GPG support
        """)
        assert search(pattern, result.out)
