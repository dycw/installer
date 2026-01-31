from __future__ import annotations

from re import escape, search
from typing import TYPE_CHECKING

from utilities.core import normalize_multi_line_str
from utilities.pytest import run_test_frac, throttle_test
from utilities.subprocess import run

from installer.apps.lib import (
    set_up_age,
    set_up_bat,
    set_up_btm,
    set_up_delta,
    setup_direnv,
    setup_dust,
    setup_eza,
    setup_fd,
    setup_fzf,
    setup_jq,
    setup_just,
    setup_neovim,
    setup_restic,
    setup_ripgrep,
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


class TestSetUpAge:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        set_up_age(path_binaries=tmp_path, force=True)

        result1 = run(str(tmp_path / "age"), "--help", return_=True)
        pattern1 = normalize_multi_line_str("""
            Usage:
                age [--encrypt] (-r RECIPIENT | -R PATH)... [--armor] [-o OUTPUT] [INPUT]
                age [--encrypt] --passphrase [--armor] [-o OUTPUT] [INPUT]
                age --decrypt [-i PATH]... [-o OUTPUT] [INPUT]
        """)
        assert search(escape(pattern1), result1) is not None, result1

        result2 = run(str(tmp_path / "age-inspect"), "--help", return_=True)
        pattern2 = normalize_multi_line_str("""
            Usage:
                age-inspect [--json] [INPUT]
        """)
        assert search(escape(pattern2), result2) is not None, result2

        result3 = run(str(tmp_path / "age-keygen"), "--help", return_=True)
        pattern3 = normalize_multi_line_str("""
            Usage:
                age-keygen [-pq] [-o OUTPUT]
                age-keygen -y [-o OUTPUT] [INPUT]
        """)
        assert search(escape(pattern3), result3) is not None, result3

        result4 = run(str(tmp_path / "age-plugin-batchpass"), "--help", return_=True)
        pattern4 = normalize_multi_line_str("""
            age-plugin-batchpass is an age plugin that enables non-interactive
            passphrase-based encryption and decryption using environment variables.
        """)
        assert search(escape(pattern4), result4) is not None, result4


class TestSetUpBat:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        set_up_bat(path_binaries=tmp_path, force=True)
        result = run(str(tmp_path / "bat"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            Usage: bat [OPTIONS] [FILE]...
                   bat <COMMAND>
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpBtm:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        set_up_btm(path_binaries=tmp_path, force=True)
        result = run(str(tmp_path / "btm"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            Usage: btm [OPTIONS]
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpDelta:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        set_up_delta(path_binaries=tmp_path, force=True)
        result = run(str(tmp_path / "delta"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            Usage: delta [OPTIONS] [MINUS_FILE] [PLUS_FILE]
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpDirenv:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        setup_direnv(path_binaries=tmp_path, home=tmp_path)
        result = run(str(tmp_path / "direnv"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            Usage: direnv COMMAND [...ARGS]
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpDust:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        setup_dust(path_binaries=tmp_path)
        result = run(str(tmp_path / "dust"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            Usage: dust [OPTIONS] [PATH]...
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpEza:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=2 * THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        setup_eza(path_binaries=tmp_path)
        result = run(str(tmp_path / "eza"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            Usage:
              eza [options] [files...]
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpFd:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        setup_fd(path_binaries=tmp_path)
        result = run(str(tmp_path / "fd"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            Usage: fd [OPTIONS] [pattern] [path]...
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpFzf:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        setup_fzf(path_binaries=tmp_path, home=tmp_path)
        result = run(str(tmp_path / "fzf"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            Usage: fzf [options]
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpJq:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        setup_jq(force=True, path_binaries=tmp_path)
        result = run(str(tmp_path / "jq"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            Usage:\tjq [options] <jq filter> [file...]
            \tjq [options] --args <jq filter> [strings...]
            \tjq [options] --jsonargs <jq filter> [JSON_TEXTS...]
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpJust:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        setup_just(path_binaries=tmp_path)
        result = run(str(tmp_path / "just"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            Usage: just [OPTIONS] [ARGUMENTS]...
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpNeovim:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        setup_neovim(path_binaries=tmp_path)
        result = run(str(tmp_path / "nvim"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            Usage:
              nvim [options] [file ...]
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpRestic:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        setup_restic(path_binaries=tmp_path)
        result = run(str(tmp_path / "restic"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            Usage:
              restic [command]
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpRipgrep:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        setup_ripgrep(path_binaries=tmp_path)
        result = run(str(tmp_path / "rg"), "--help", return_=True)
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
        assert search(escape(pattern), result) is not None, result


class TestSetUpRuff:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        setup_ruff(path_binaries=tmp_path)
        result = run(str(tmp_path / "ruff"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            Usage: ruff [OPTIONS] <COMMAND>
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpSd:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        setup_sd(path_binaries=tmp_path)
        result = run(str(tmp_path / "sd"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            Usage: sd [OPTIONS] <FIND> <REPLACE_WITH> [FILES]...
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpShellcheck:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        setup_shellcheck(path_binaries=tmp_path)
        result = run(str(tmp_path / "shellcheck"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            Usage: shellcheck [OPTIONS...] FILES...
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpShfmt:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        setup_shfmt(path_binaries=tmp_path)
        result = run(str(tmp_path / "shfmt"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            usage: shfmt [flags] [path ...]
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpSops:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        setup_sops(path_binaries=tmp_path)
        result = run(str(tmp_path / "sops"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            NAME:
               sops - sops - encrypted file editor with AWS KMS, GCP KMS, Azure Key Vault, age, and GPG support
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpStarship:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        setup_starship(path_binaries=tmp_path, home=tmp_path)
        result = run(str(tmp_path / "starship"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            Usage: starship <COMMAND>
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpTaplo:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        setup_taplo(path_binaries=tmp_path)
        result = run(str(tmp_path / "taplo"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            Usage: taplo [OPTIONS] <COMMAND>
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpUv:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        setup_uv(path_binaries=tmp_path)
        result = run(str(tmp_path / "uv"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            Usage: uv [OPTIONS] <COMMAND>
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpUvCmd:
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


class TestSetUpWatchexec:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        setup_watchexec(path_binaries=tmp_path)
        result = run(str(tmp_path / "watchexec"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            Usage: watchexec [OPTIONS] [COMMAND]...
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpYq:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        setup_yq(path_binaries=tmp_path)
        result = run(str(tmp_path / "yq"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            Usage:
              yq [flags]
              yq [command]
        """)
        assert search(escape(pattern), result) is not None, result


class TestSetUpZoxide:
    @run_test_frac(frac=RUN_TEST_FRAC)
    @throttle_test(duration=THROTTLE_DURATION)
    def test_main(self, *, tmp_path: Path) -> None:
        setup_zoxide(force=True, path_binaries=tmp_path, home=tmp_path)
        result = run(str(tmp_path / "zoxide"), "--help", return_=True)
        pattern = normalize_multi_line_str("""
            Usage:
              zoxide <COMMAND>
        """)
        assert search(escape(pattern), result) is not None, result
