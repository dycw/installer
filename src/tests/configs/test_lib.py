from __future__ import annotations

from re import search
from typing import TYPE_CHECKING

from pytest import raises
from utilities.core import normalize_multi_line_str

from installer.configs.lib import (
    set_up_authorized_keys,
    set_up_shell_config,
    set_up_ssh_config,
    set_up_sshd_config,
    sshd_config,
)

if TYPE_CHECKING:
    from pathlib import Path


class TestSetUpAuthorizedKeys:
    def test_main(self, *, tmp_path: Path) -> None:
        set_up_authorized_keys(["key1", "key2"], home=tmp_path)
        path = tmp_path / ".ssh/authorized_keys"
        assert path.is_file()
        assert len(path.read_text().splitlines()) == 2


class TestSetUpSSHConfig:
    def test_main(self, *, tmp_path: Path) -> None:
        set_up_ssh_config(home=tmp_path)
        config = tmp_path / ".ssh/config"
        assert config.is_file()
        assert search(r"^Include .*/\*\.conf$", config.read_text())
        config_d = tmp_path / ".ssh/config.d"
        assert config_d.is_dir()
        assert len(list(config_d.iterdir())) == 0


class TestSetUpSSHDConfig:
    def test_main(self, *, tmp_path: Path) -> None:
        set_up_sshd_config(root=tmp_path)
        path = tmp_path / "etc/ssh/sshd_config.d/default.conf"
        assert path.is_file()
        assert path.read_text() == sshd_config()


class TestSetUpShellConfig:
    def test_home_bash(self, *, tmp_path: Path) -> None:
        set_up_shell_config("bash", "zsh", "fish", shell="bash", home=tmp_path)  # noqa: S604
        path = tmp_path / ".bashrc"
        assert path.read_text() == "bash\n"

    def test_home_zsh(self, *, tmp_path: Path) -> None:
        set_up_shell_config("bash", "zsh", "fish", shell="zsh", home=tmp_path)  # noqa: S604
        path = tmp_path / ".zshrc"
        assert path.read_text() == "zsh\n"

    def test_home_fish(self, *, tmp_path: Path) -> None:
        set_up_shell_config("bash", "zsh", "fish", shell="fish", home=tmp_path)  # noqa: S604
        path = tmp_path / ".config/fish/config.fish"
        assert path.read_text() == "fish\n"

    def test_etc_bash_single(self, *, tmp_path: Path) -> None:
        set_up_shell_config(  # noqa: S604
            "bash", "zsh", "fish", shell="bash", etc="etc", root=tmp_path
        )
        path = tmp_path / "etc/profile.d/etc.sh"
        assert path.read_text() == normalize_multi_line_str("""
           #!/usr/bin/env sh

           bash
        """)

    def test_etc_bash_multiple(self, *, tmp_path: Path) -> None:
        set_up_shell_config(  # noqa: S604
            ["bash 1", "bash 2"], "zsh", "fish", shell="bash", etc="etc", root=tmp_path
        )
        path = tmp_path / "etc/profile.d/etc.sh"
        assert path.read_text() == normalize_multi_line_str("""
           #!/usr/bin/env sh

           bash 1
           bash 2
        """)

    def test_error_etc_zsh(self) -> None:
        with raises(ValueError, match="Invalid shell for 'etc': 'zsh'"):
            set_up_shell_config(  # noqa: S604
                "bash", " zsh", "fish", shell="zsh", etc="etc"
            )


class TestSSHDConfig:
    def test_main(self) -> None:
        result = sshd_config()
        expected = normalize_multi_line_str("""
            PasswordAuthentication no
            PermitRootLogin no
            PubkeyAcceptedAlgorithms ssh-ed25519
            PubkeyAuthentication yes
        """)
        assert result == expected
