from __future__ import annotations

from typing import TYPE_CHECKING

from pytest import raises
from utilities.core import normalize_multi_line_str

from installer.configs.lib import (
    setup_authorized_keys,
    setup_shell_config,
    setup_ssh_config,
    setup_sshd_config,
    sshd_config,
)

if TYPE_CHECKING:
    from pathlib import Path


class TestSetupAuthorizedKeys:
    def test_main(self, *, tmp_path: Path) -> None:
        setup_authorized_keys([], home=tmp_path)


class TestSetupSSHConfig:
    def test_main(self, *, tmp_path: Path) -> None:
        setup_ssh_config(home=tmp_path)


class TestSetupSSHDConfig:
    def test_main(self, *, tmp_path: Path) -> None:
        setup_sshd_config(root=tmp_path)


class TestSetupShellConfig:
    def test_home_bash(self, *, tmp_path: Path) -> None:
        setup_shell_config("bash", "zsh", "fish", shell="bash", home=tmp_path)  # noqa: S604
        path = tmp_path / ".bashrc"
        assert path.read_text() == "bash\n"

    def test_home_zsh(self, *, tmp_path: Path) -> None:
        setup_shell_config("bash", "zsh", "fish", shell="zsh", home=tmp_path)  # noqa: S604
        path = tmp_path / ".zshrc"
        assert path.read_text() == "zsh\n"

    def test_home_fish(self, *, tmp_path: Path) -> None:
        setup_shell_config("bash", "zsh", "fish", shell="fish", home=tmp_path)  # noqa: S604
        path = tmp_path / ".config/fish/config.fish"
        assert path.read_text() == "fish\n"

    def test_etc_bash_single(self, *, tmp_path: Path) -> None:
        setup_shell_config(  # noqa: S604
            "bash", "zsh", "fish", shell="bash", etc="etc", root=tmp_path
        )
        path = tmp_path / "etc/profile.d/etc.sh"
        assert path.read_text() == normalize_multi_line_str("""
           #!/usr/bin/env sh

           bash
        """)

    def test_etc_bash_multiple(self, *, tmp_path: Path) -> None:
        setup_shell_config(  # noqa: S604
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
            setup_shell_config(  # noqa: S604
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
