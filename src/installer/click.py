from __future__ import annotations

from click import option

logger_option = option("--logger", type=str, default=None, help="Logger name")
ssh_option = option("--ssh", type=str, default=None, help="SSH user & hostname")
sudo_option = option("--sudo", is_flag=True, default=False, help="Run as 'sudo'")
retry_option = option("--ssh", type=tuple[int, int], default=None, help="SSH retry")


__all__ = ["logger_option", "retry_option", "ssh_option", "sudo_option"]
