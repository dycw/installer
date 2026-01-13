from __future__ import annotations

from re import escape, search
from typing import TYPE_CHECKING

from utilities.pytest import throttle_test
from utilities.subprocess import run
from utilities.text import strip_and_dedent
from utilities.whenever import HOUR

from installer.lib import (
    setup_age,
    setup_bottom,
    setup_direnv,
    setup_fd,
    setup_fzf,
    setup_jq,
    setup_just,
    setup_restic,
    setup_ripgrep,
    setup_sd,
    setup_shellcheck,
    setup_shfmt,
    setup_sops,
    setup_starship,
    setup_yq,
    setup_zoxide,
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
        pattern1 = strip_and_dedent("""
            Clement Tsang <cjhtsang@uwaterloo.ca>

            A customizable cross-platform graphical process/system monitor for the terminal. Supports Linux,
            macOS, and Windows.

            Usage: btm [OPTIONS]
        """)
        pattern2 = strip_and_dedent("""
            Clement Tsang <cjhtsang@uwaterloo.ca>

            A customizable cross-platform graphical process/system monitor for the terminal.
            Supports Linux, macOS, and Windows.

            Usage: btm [OPTIONS]
        """)
        assert any(search(escape(p), result.out) for p in [pattern1, pattern2])


class TestSetupDirenv:
    @throttle_test(delta=HOUR)
    def test_main(
        self, *, token: Secret[str] | None, tmp_path: Path, capsys: CaptureFixture
    ) -> None:
        setup_direnv(token=token, path_binaries=tmp_path, skip_shell_rc=True)
        run(str(tmp_path / "direnv"), "--help", print=True)
        result = capsys.readouterr()
        pattern = strip_and_dedent("""
            Usage: direnv COMMAND [...ARGS]
        """)
        assert search(escape(pattern), result.out)


class TestSetupFd:
    @throttle_test(delta=HOUR)
    def test_main(
        self, *, token: Secret[str] | None, tmp_path: Path, capsys: CaptureFixture
    ) -> None:
        setup_fd(token=token, path_binaries=tmp_path)
        run(str(tmp_path / "fd"), "--help", print=True)
        result = capsys.readouterr()
        pattern = strip_and_dedent("""
            A program to find entries in your filesystem

            Usage: fd [OPTIONS] [pattern] [path]...
        """)
        assert search(escape(pattern), result.out)


class TestSetupFzf:
    @throttle_test(delta=HOUR)
    def test_main(
        self, *, token: Secret[str] | None, tmp_path: Path, capsys: CaptureFixture
    ) -> None:
        setup_fzf(token=token, path_binaries=tmp_path, skip_shell_rc=True)
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


class TestSetupJq:
    @throttle_test(delta=HOUR)
    def test_main(
        self, *, token: Secret[str] | None, tmp_path: Path, capsys: CaptureFixture
    ) -> None:
        setup_jq(token=token, path_binaries=tmp_path)
        run(str(tmp_path / "jq"), "--help", print=True)
        result = capsys.readouterr()
        pattern = strip_and_dedent("""
            Usage:\tjq [options] <jq filter> [file...]
            \tjq [options] --args <jq filter> [strings...]
            \tjq [options] --jsonargs <jq filter> [JSON_TEXTS...]

            jq is a tool for processing JSON inputs, applying the given filter to
            its JSON text inputs and producing the filter's results as JSON on
            standard output.

            The simplest filter is ., which copies jq's input to its output
            unmodified except for formatting. For more advanced filters see
            the jq(1) manpage ("man jq") and/or https://jqlang.org/.
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


class TestSetupSd:
    @throttle_test(delta=HOUR)
    def test_main(
        self, *, token: Secret[str] | None, tmp_path: Path, capsys: CaptureFixture
    ) -> None:
        setup_sd(token=token, path_binaries=tmp_path)
        run(str(tmp_path / "sd"), "--help", print=True)
        result = capsys.readouterr()
        pattern = strip_and_dedent("""
            An intuitive find & replace CLI

            Usage: sd [OPTIONS] <FIND> <REPLACE_WITH> [FILES]...
        """)
        assert search(escape(pattern), result.out)


class TestSetupShellcheck:
    @throttle_test(delta=HOUR)
    def test_main(
        self, *, token: Secret[str] | None, tmp_path: Path, capsys: CaptureFixture
    ) -> None:
        setup_shellcheck(token=token, path_binaries=tmp_path)
        run(str(tmp_path / "shellcheck"), "--help", print=True)
        result = capsys.readouterr()
        pattern = strip_and_dedent("""
            Usage: shellcheck [OPTIONS...] FILES...
        """)
        assert search(escape(pattern), result.out)


class TestSetupShfmt:
    @throttle_test(delta=HOUR)
    def test_main(
        self, *, token: Secret[str] | None, tmp_path: Path, capsys: CaptureFixture
    ) -> None:
        setup_shfmt(token=token, path_binaries=tmp_path)
        run(str(tmp_path / "shfmt"), "--help", print=True)
        result = capsys.readouterr()
        pattern = strip_and_dedent("""
            usage: shfmt [flags] [path ...]

            shfmt formats shell programs. If the only argument is a dash ('-') or no
            arguments are given, standard input will be used. If a given path is a
            directory, all shell scripts found under that directory will be used.
        """)
        assert search(escape(pattern), result.err)


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
        setup_starship(token=token, path_binaries=tmp_path, skip_shell_rc=True)
        run(str(tmp_path / "starship"), "--help", print=True)
        result = capsys.readouterr()
        pattern = strip_and_dedent("""
            The cross-shell prompt for astronauts. ☄🌌️

            Usage: starship <COMMAND>
        """)
        assert search(escape(pattern), result.out)


class TestSetupYq:
    @throttle_test(delta=HOUR)
    def test_main(
        self, *, token: Secret[str] | None, tmp_path: Path, capsys: CaptureFixture
    ) -> None:
        setup_yq(token=token, path_binaries=tmp_path)
        run(str(tmp_path / "yq"), "--help", print=True)
        result = capsys.readouterr()
        pattern = strip_and_dedent("""
            yq is a portable command-line data file processor (https://github.com/mikefarah/yq/)
        """)
        assert search(escape(pattern), result.out)


class TestSetupZoxide:
    @throttle_test(delta=HOUR)
    def test_main(
        self, *, token: Secret[str] | None, tmp_path: Path, capsys: CaptureFixture
    ) -> None:
        setup_zoxide(token=token, path_binaries=tmp_path, skip_shell_rc=True)
        run(str(tmp_path / "zoxide"), "--help", print=True)
        result = capsys.readouterr()
        pattern = strip_and_dedent("""
            Ajeet D'Souza <98ajeet@gmail.com>
            https://github.com/ajeetdsouza/zoxide

            A smarter cd command for your terminal

            Usage:
              zoxide <COMMAND>
        """)
        assert search(escape(pattern), result.out)
