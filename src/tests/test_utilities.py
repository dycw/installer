from __future__ import annotations

from pytest import mark, param

from installer.utilities import split_ssh


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
