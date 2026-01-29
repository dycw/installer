from __future__ import annotations

from re import escape, search
from typing import TYPE_CHECKING

from pytest import mark
from utilities.core import normalize_multi_line_str
from utilities.pytest import run_test_frac, skipif_not_linux, throttle_test
from utilities.subprocess import run

from installer.apps.lib import (
    setup_age,
    setup_bat,
    setup_bottom,
    setup_curl,
    setup_delta,
    setup_direnv,
    setup_dust,
    setup_eza,
    setup_fd,
    setup_fzf,
    setup_git,
    setup_jq,
    setup_just,
    setup_neovim,
    setup_restic,
    setup_ripgrep,
    setup_rsync,
    setup_ruff,
    setup_sd,
    setup_shellcheck,
    setup_shfmt,
    setup_sops,
    setup_starship,
    setup_taplo,
    setup_uv,
    setup_uv_cmd,
    setup_watchexec,
    setup_yq,
    setup_zoxide,
)
from tests.conftest import RUN_TEST_FRAC, THROTTLE_DURATION

if TYPE_CHECKING:
    from pathlib import Path

    from pytest import CaptureFixture


class TestSetupAge:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_age(path_binaries=tmp_path)

        run(str(tmp_path / "age"), "--help", print=True)
        result1 = capsys.readouterr()
        pattern1 = normalize_multi_line_str("""
            Usage:
                age [--encrypt] (-r RECIPIENT | -R PATH)... [--armor] [-o OUTPUT] [INPUT]
                age [--encrypt] --passphrase [--armor] [-o OUTPUT] [INPUT]
                age --decrypt [-i PATH]... [-o OUTPUT] [INPUT]
        """)
        assert search(escape(pattern1), result1.err) is not None, result1.err

        run(str(tmp_path / "age-inspect"), "--help", print=True)
        result2 = capsys.readouterr()
        pattern2 = normalize_multi_line_str("""
            Usage:
                age-inspect [--json] [INPUT]
        """)
        assert search(escape(pattern2), result2.err) is not None, result2.err

        run(str(tmp_path / "age-keygen"), "--help", print=True)
        result3 = capsys.readouterr()
        pattern3 = normalize_multi_line_str("""
            Usage:
                age-keygen [-pq] [-o OUTPUT]
                age-keygen -y [-o OUTPUT] [INPUT]
        """)
        assert search(escape(pattern3), result3.err) is not None, result3.err

        run(str(tmp_path / "age-plugin-batchpass"), "--help", print=True)
        result4 = capsys.readouterr()
        pattern4 = normalize_multi_line_str("""
            age-plugin-batchpass is an age plugin that enables non-interactive
            passphrase-based encryption and decryption using environment variables.
        """)
        assert search(escape(pattern4), result4.err) is not None, result4.err


class TestSetupBottom:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_bottom(path_binaries=tmp_path)
        run(str(tmp_path / "btm"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usage: btm [OPTIONS]
        """)
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupBat:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_bat(path_binaries=tmp_path)
        run(str(tmp_path / "bat"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usage: bat [OPTIONS] [FILE]...
                   bat <COMMAND>
        """)
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupCurl:
    @mark.only
    @run_test_frac(frac=RUN_TEST_FRAC)
    @skipif_not_linux
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, capsys: CaptureFixture) -> None:
        setup_curl()
        run("curl", "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Uscurl:
                curl [--encrypt] (-r RECIPIENT | -R PATH)... [--armor] [-o OUTPUT] [INPUT]
                curl [--encrypt] --passphrase [--armor] [-o OUTPUT] [INPUT]
                curl --decrypt [-i PATH]... [-o OUTPUT] [INPUT]
        """)
        assert search(escape(pattern), result.err) is not None, result.err


class TestSetupDelta:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_delta(path_binaries=tmp_path)
        run(str(tmp_path / "delta"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usage: delta [OPTIONS] [MINUS_FILE] [PLUS_FILE]
        """)
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupDirenv:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_direnv(path_binaries=tmp_path, home=tmp_path)
        run(str(tmp_path / "direnv"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usage: direnv COMMAND [...ARGS]
        """)
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupDust:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_dust(path_binaries=tmp_path)
        run(str(tmp_path / "dust"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usage: dust [OPTIONS] [PATH]...
        """)
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupEza:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=2 * THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_eza(path_binaries=tmp_path)
        run(str(tmp_path / "eza"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usage:
              eza [options] [files...]
        """)
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupFd:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_fd(path_binaries=tmp_path)
        run(str(tmp_path / "fd"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usage: fd [OPTIONS] [pattern] [path]...
        """)
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupFzf:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_fzf(path_binaries=tmp_path, home=tmp_path)
        run(str(tmp_path / "fzf"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usage: fzf [options]
        """)
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupGit:
    @mark.only
    @run_test_frac(frac=RUN_TEST_FRAC)
    @skipif_not_linux
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, capsys: CaptureFixture) -> None:
        setup_git()
        run("git", "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usgit:
                git [--encrypt] (-r RECIPIENT | -R PATH)... [--armor] [-o OUTPUT] [INPUT]
                git [--encrypt] --passphrase [--armor] [-o OUTPUT] [INPUT]
                git --decrypt [-i PATH]... [-o OUTPUT] [INPUT]
        """)
        assert search(escape(pattern), result.err) is not None, result.err


class TestSetupJq:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_jq(path_binaries=tmp_path)
        run(str(tmp_path / "jq"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usage:\tjq [options] <jq filter> [file...]
            \tjq [options] --args <jq filter> [strings...]
            \tjq [options] --jsonargs <jq filter> [JSON_TEXTS...]
        """)
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupJust:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_just(path_binaries=tmp_path)
        run(str(tmp_path / "just"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usage: just [OPTIONS] [ARGUMENTS]...
        """)
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupNeovim:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_neovim(path_binaries=tmp_path)
        run(str(tmp_path / "nvim"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usage:
              nvim [options] [file ...]
        """)
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupRestic:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_restic(path_binaries=tmp_path)
        run(str(tmp_path / "restic"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usage:
              restic [command]
        """)
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupRipgrep:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_ripgrep(path_binaries=tmp_path)
        run(str(tmp_path / "rg"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
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
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupRsync:
    @mark.only
    @run_test_frac(frac=RUN_TEST_FRAC)
    @skipif_not_linux
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, capsys: CaptureFixture) -> None:
        setup_rsync()
        run("rsync", "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usrsync:
                rsync [--encrypt] (-r RECIPIENT | -R PATH)... [--armor] [-o OUTPUT] [INPUT]
                rsync [--encrypt] --passphrase [--armor] [-o OUTPUT] [INPUT]
                rsync --decrypt [-i PATH]... [-o OUTPUT] [INPUT]
        """)
        assert search(escape(pattern), result.err) is not None, result.err


class TestSetupRuff:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_ruff(path_binaries=tmp_path)
        run(str(tmp_path / "ruff"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usage: ruff [OPTIONS] <COMMAND>
        """)
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupSd:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_sd(path_binaries=tmp_path)
        run(str(tmp_path / "sd"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usage: sd [OPTIONS] <FIND> <REPLACE_WITH> [FILES]...
        """)
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupShellcheck:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_shellcheck(path_binaries=tmp_path)
        run(str(tmp_path / "shellcheck"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usage: shellcheck [OPTIONS...] FILES...
        """)
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupShfmt:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_shfmt(path_binaries=tmp_path)
        run(str(tmp_path / "shfmt"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            usage: shfmt [flags] [path ...]
        """)
        assert search(escape(pattern), result.err) is not None, result.err


class TestSetupSops:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_sops(path_binaries=tmp_path)
        run(str(tmp_path / "sops"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            NAME:
               sops - sops - encrypted file editor with AWS KMS, GCP KMS, Azure Key Vault, age, and GPG support
        """)
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupStarship:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_starship(path_binaries=tmp_path, home=tmp_path)
        run(str(tmp_path / "starship"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usage: starship <COMMAND>
        """)
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupTaplo:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_taplo(path_binaries=tmp_path)
        run(str(tmp_path / "taplo"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usage: taplo [OPTIONS] <COMMAND>
        """)
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupUv:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_uv(path_binaries=tmp_path)
        run(str(tmp_path / "uv"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usage: uv [OPTIONS] <COMMAND>
        """)
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupUvCmd:
    def test_main(self, *, tmp_path: Path) -> None:
        result = setup_uv_cmd(tmp_path)
        path = tmp_path / "install.sh"
        expected = normalize_multi_line_str(f"""
            curl --fail --location --create-dirs --output {path} --show-error --silent https://astral.sh/uv/install.sh
            env UV_INSTALL_DIR=/usr/local/bin UV_NO_MODIFY_PATH=1 sh {path}
        """)
        assert result == expected

    def test_path_binaries(self, *, tmp_path: Path) -> None:
        result = setup_uv_cmd(tmp_path, path_binaries=tmp_path / "bin")
        path = tmp_path / "install.sh"
        expected = normalize_multi_line_str(f"""
            curl --fail --location --create-dirs --output {path} --show-error --silent https://astral.sh/uv/install.sh
            env UV_INSTALL_DIR={tmp_path}/bin UV_NO_MODIFY_PATH=1 sh {path}
        """)
        assert result == expected

    def test_sudo(self, *, tmp_path: Path) -> None:
        result = setup_uv_cmd(tmp_path, sudo=True)
        path = tmp_path / "install.sh"
        expected = normalize_multi_line_str(f"""
            curl --fail --location --create-dirs --output {path} --show-error --silent https://astral.sh/uv/install.sh
            sudo env UV_INSTALL_DIR=/usr/local/bin UV_NO_MODIFY_PATH=1 sh {path}
        """)
        assert result == expected


class TestSetupWatchexec:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_watchexec(path_binaries=tmp_path)
        run(str(tmp_path / "watchexec"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usage: watchexec [OPTIONS] [COMMAND]...
        """)
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupYq:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_yq(path_binaries=tmp_path)
        run(str(tmp_path / "yq"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usage:
              yq [flags]
              yq [command]
        """)
        assert search(escape(pattern), result.out) is not None, result.out


class TestSetupZoxide:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path, capsys: CaptureFixture) -> None:
        setup_zoxide(path_binaries=tmp_path, home=tmp_path)
        run(str(tmp_path / "zoxide"), "--help", print=True)
        result = capsys.readouterr()
        pattern = normalize_multi_line_str("""
            Usage:
              zoxide <COMMAND>
        """)
        assert search(escape(pattern), result.out) is not None, result.out
