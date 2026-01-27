from __future__ import annotations

from typing import TYPE_CHECKING

from pytest import mark, param

from installer.utilities import ensure_line_or_lines, split_ssh

if TYPE_CHECKING:
    from pathlib import Path


class TestEnsureLineOrLines:
    def test_single_write(self, *, tmp_path: Path) -> None:
        path = tmp_path / "file.txt"
        ensure_line_or_lines(path, "text")
        assert path.read_text() == "text\n"

    def test_single_append(self, *, tmp_path: Path) -> None:
        path = tmp_path / "file.txt"
        _ = path.write_text("line 1")
        ensure_line_or_lines(path, "line 2")
        assert path.read_text() == "line 1\n\nline 2\n"

    def test_multiple_write(self, *, tmp_path: Path) -> None:
        path = tmp_path / "file.txt"
        ensure_line_or_lines(path, ["line 1", "line 2"])
        assert path.read_text() == "line 1\nline 2\n"

    def test_multiple_append(self, *, tmp_path: Path) -> None:
        path = tmp_path / "file.txt"
        _ = path.write_text("line 1\nline 2")
        ensure_line_or_lines(path, ["line 3", "line 4"])
        assert path.read_text() == "line 1\nline 2\n\nline 3\nline 4\n"


class TestSplitSSH:
    @mark.parametrize(
        ("ssh", "exp_user", "exp_hostname"),
        [
            param("user@hostname", "user", "hostname"),
            param("user@hostname.subnet", "user", "hostname.subnet"),
        ],
    )
    def test_main(self, *, ssh: str, exp_user: str, exp_hostname: str) -> None:
        res_user, res_hostname = split_ssh(ssh)
        assert res_user == exp_user
        assert res_hostname == exp_hostname
