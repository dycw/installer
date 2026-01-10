from __future__ import annotations

from re import escape, search
from typing import TYPE_CHECKING

from utilities.pytest import throttle_test
from utilities.subprocess import run
from utilities.text import strip_and_dedent
from utilities.whenever import HOUR

from github_downloader.lib import (
    setup_age,
    setup_bottom,
    setup_direnv,
    setup_fzf,
    setup_just,
    setup_restic,
    setup_ripgrep,
    setup_sops,
    setup_starship,
)

if TYPE_CHECKING:
    from pathlib import Path

    from pytest import CaptureFixture
    from typed_settings import Secret


class TestSetupAge:
    @throttle_test(delta=HOUR)
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


class TestSetupBottom:
    @throttle_test(delta=HOUR)
    def test_main(
        self, *, token: Secret[str] | None, tmp_path: Path, capsys: CaptureFixture
    ) -> None:
        setup_bottom(token=token, path_binaries=tmp_path)
        run(str(tmp_path / "btm"), "--help", print=True)
        result = capsys.readouterr()
        pattern = strip_and_dedent("""
            Clement Tsang <cjhtsang@uwaterloo.ca>

            A customizable cross-platform graphical process/system monitor for the terminal.
            Supports Linux, macOS, and Windows.

            Usage: btm [OPTIONS]
        """)
        assert search(escape(pattern), result.out)


class TestSetupDirenv:
    @throttle_test(delta=HOUR)
    def test_main(
        self, *, token: Secret[str] | None, tmp_path: Path, capsys: CaptureFixture
    ) -> None:
        setup_direnv(token=token, path_binaries=tmp_path)
        run(str(tmp_path / "direnv"), "--help", print=True)
        result = capsys.readouterr()
        pattern = strip_and_dedent("""
            Usage: direnv COMMAND [...ARGS]
        """)
        assert search(escape(pattern), result.out)


class TestSetupFzf:
    @throttle_test(delta=HOUR)
    def test_main(
        self, *, token: Secret[str] | None, tmp_path: Path, capsys: CaptureFixture
    ) -> None:
        setup_fzf(token=token, path_binaries=tmp_path)
        run(str(tmp_path / "fzf"), "--help", print=True)
        result = capsys.readouterr()
        pattern = strip_and_dedent("""
            fzf is an interactive filter program for any kind of list.

            It implements a "fuzzy" matching algorithm, so you can quickly type in patterns
            with omitted characters and still get the results you want.

            Project URL: https://github.com/junegunn/fzf
            Author: Junegunn Choi <junegunn.c@gmail.com>

            * See man page for more information: fzf --man

            Usage: fzf [options]
        """)
        assert search(escape(pattern), result.out)


class TestSetupJust:
    @throttle_test(delta=HOUR)
    def test_main(
        self, *, token: Secret[str] | None, tmp_path: Path, capsys: CaptureFixture
    ) -> None:
        setup_just(token=token, path_binaries=tmp_path)
        run(str(tmp_path / "just"), "--help", print=True)
        result = capsys.readouterr()
        pattern = strip_and_dedent("""
            🤖 Just a command runner - https://github.com/casey/just

            Usage: just [OPTIONS] [ARGUMENTS]...
        """)
        assert search(escape(pattern), result.out)


class TestSetupRestic:
    @throttle_test(delta=HOUR)
    def test_main(
        self, *, token: Secret[str] | None, tmp_path: Path, capsys: CaptureFixture
    ) -> None:
        setup_restic(token=token, path_binaries=tmp_path)
        run(str(tmp_path / "restic"), "--help", print=True)
        result = capsys.readouterr()
        pattern = strip_and_dedent("""
            restic is a backup program which allows saving multiple revisions of files and
            directories in an encrypted repository stored on different backends.

            The full documentation can be found at https://restic.readthedocs.io/ .

            Usage:
              restic [command]
        """)
        assert search(escape(pattern), result.out)


class TestSetupRipgrep:
    @throttle_test(delta=HOUR)
    def test_main(
        self, *, token: Secret[str] | None, tmp_path: Path, capsys: CaptureFixture
    ) -> None:
        setup_ripgrep(token=token, path_binaries=tmp_path)
        run(str(tmp_path / "rg"), "--help", print=True)
        result = capsys.readouterr()
        pattern = strip_and_dedent("""
            ripgrep (rg) recursively searches the current directory for lines matching
            a regex pattern. By default, ripgrep will respect gitignore rules and
            automatically skip hidden files/directories and binary files.

            Use -h for short descriptions and --help for more details.

            Project home page: https://github.com/BurntSushi/ripgrep

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
    @throttle_test(delta=HOUR)
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
        assert search(escape(pattern), result.out)


class TestSetupStarship:
    @throttle_test(delta=HOUR)
    def test_main(
        self, *, token: Secret[str] | None, tmp_path: Path, capsys: CaptureFixture
    ) -> None:
        setup_starship(token=token, path_binaries=tmp_path)
        run(str(tmp_path / "starship"), "--help", print=True)
        result = capsys.readouterr()
        pattern = strip_and_dedent("""
            The cross-shell prompt for astronauts. ☄🌌️

            Usage: starship <COMMAND>
        """)
        assert search(escape(pattern), result.out)
