from __future__ import annotations

import shutil
import tarfile
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager, suppress
from grp import getgrgid
from logging import getLogger
from os import environ, getegid, getenv, geteuid
from pathlib import Path
from pwd import getpwuid
from re import search
from stat import S_IXUSR
from string import Template
from subprocess import check_output
from typing import TYPE_CHECKING, Any
from urllib.parse import urlparse
from urllib.request import urlopen

if TYPE_CHECKING:
    from collections.abc import Iterator, Mapping
    from types import TracebackType

    from .types import PathLike


_LOGGER = getLogger(__name__)
SOURCE_BASHRC = "if [ -f ~/.bashrc ]; then source ~/.bashrc; fi"
EVAL_DIRENV_EXPORT = (
    'if command -v direnv >/dev/null 2>&1; then eval "$(direnv export bash)"; fi'
)


def append_contents(
    path: PathLike, text: str, /, *, skip_log: bool = False, new_lines: int = 1
) -> None:
    path = full_path(path)
    if path.exists():
        if text in path.read_text():
            return
        if not skip_log:
            _LOGGER.info("Appending %r text to %r...", text, str(path))
        with path.open(mode="a") as fh:
            _ = fh.write(new_lines * "\n")
            _ = fh.write(text)
        return
    write_text(text, path, skip_log=skip_log)


def apt_install(*packages: str, env: Mapping[str, str | None] | None = None) -> None:
    check_for_commands("apt")
    apt_update()
    desc = ", ".join(map(repr, packages))
    _LOGGER.info("Installing %s...", desc)
    joined = " ".join(packages)
    cmd = f"sudo apt -y install {joined}"
    _ = run_command(cmd, env=env)


def apt_update() -> None:
    check_for_commands("apt")
    _LOGGER.info("Updating 'apt'...")
    _ = run_command("sudo apt -y update")


def brew_install(*packages: str, cask: bool = False) -> None:
    check_for_commands("brew")
    _LOGGER.info("Updating 'brew'...")
    _ = run_command("brew update")
    desc = ", ".join(map(repr, packages))
    _LOGGER.info("Installing %s...", desc)
    cmd = "brew install"
    if cask:
        cmd = f"{cmd} --cask"
    joined = " ".join(packages)
    cmd = f"{cmd} {joined}"
    _ = run_command(cmd)


def brew_installed(package: str, /) -> bool:
    check_for_commands("brew")
    output = run_command("brew list -1")
    return any(p == package for p in output.splitlines())


def check_for_commands(*cmds: str) -> None:
    missing = [c for c in cmds if not have_command(c)]
    if len(missing) >= 1:
        all_ = ", ".join(map(repr, cmds))
        missing_ = ", ".join(map(repr, missing))
        msg = f"Must have commands {all_}, but {missing_} are missing"
        raise RuntimeError(msg)


def chmod(path: PathLike, /, *, skip_log: bool = False) -> None:
    path = full_path(path)
    mode = path.stat().st_mode
    if mode & S_IXUSR:
        return
    _ = run_command(f"sudo chmod u+x {path}", skip_log=skip_log)


def chown(path: PathLike, /, *, skip_log: bool = False) -> None:
    path = full_path(path)
    stat = path.stat()
    file_user, curr_user = [getpwuid(i).pw_name for i in [stat.st_uid, geteuid()]]
    file_group, curr_group = [getgrgid(i).gr_name for i in [stat.st_gid, getegid()]]
    if (file_user == curr_user) and (file_group == curr_group):
        return
    _ = run_command(f"sudo chown {curr_user}:{curr_group} {path}", skip_log=skip_log)


def contains_line(path: PathLike, text: str, /, *, flags: int = 0) -> bool:
    try:
        contents = full_path(path).read_text()
    except FileNotFoundError:
        return False
    return any(search(text, line_i, flags=flags) for line_i in contents.splitlines())


def cp(
    path_from: PathLike,
    path_to: PathLike,
    /,
    *,
    skip_log: bool = False,
    executable: bool = False,
    immutable: bool = False,
    ownership: bool = False,
) -> None:
    path_from, path_to = map(full_path, [path_from, path_to])
    if path_to.exists() and (path_to.read_bytes() == path_from.read_bytes()):
        return
    rm(path_to, skip_log=skip_log)
    if not skip_log:
        _LOGGER.info("Copying %r -> %r...", str(path_from), str(path_to))
    _ = run_commands(
        f"sudo mkdir -p {path_to.parent}",
        f"sudo cp {path_from} {path_to}",
        skip_log=skip_log,
    )
    if executable:
        chmod(path_to, skip_log=skip_log)
    if immutable:
        _ = run_command(f"sudo chattr +i {path_to}", skip_log=skip_log)
    if ownership:
        chown(path_to, skip_log=skip_log)


def download(url: str, path: PathLike, /) -> None:
    with urlopen(url) as response, full_path(path).open(mode="wb") as fh:
        _ = fh.write(response.read())


def dpkg_install(path: PathLike, /) -> None:
    check_for_commands("dpkg")
    _ = run_command(f"sudo dpkg -i {path}")


def full_path(*parts: PathLike) -> Path:
    return Path(*parts).expanduser()


def get_latest_tag(owner: str, repo: str, /) -> str:
    check_for_commands("curl", "jq")
    _LOGGER.info("Getting latest tag '%s/%s'...", owner, repo)
    return run_command(
        f"curl -s https://api.github.com/repos/{owner}/{repo}/releases/latest | jq -r '.tag_name'"
    )


def git_pull(*, cwd: PathLike | None = None) -> None:
    _LOGGER.info("Pulling 'git'...")
    _ = run_command("git pull", cwd=cwd)


def have_command(cmd: str, /) -> bool:
    return which(cmd) is not None


def is_root() -> bool:
    return geteuid() == 0


def luarocks_install(package: str, /) -> None:
    check_for_commands("luarocks")
    _ = run_command(f"sudo luarocks install {package}")


def mac_app_exists(app: str, /) -> bool:
    return full_path(f"/Applications/{app}.app").is_dir()


def replace_line(
    path: PathLike, from_: str, to: str, /, *, skip_log: bool = False
) -> None:
    replace_lines(path, (from_, to), skip_log=skip_log)


def replace_lines(
    path: PathLike, /, *lines: tuple[str, str], skip_log: bool = False
) -> None:
    path = full_path(path)
    text = path.read_text()
    for from_, to in lines:
        text = text.replace(from_, to)
    write_text(text, path, skip_log=skip_log)


def rm(path: PathLike, /, *, skip_log: bool = False) -> None:
    path = full_path(path)
    if not path.exists():
        return
    _ = run_command(f"sudo rm {path}", skip_log=skip_log)


def run_command(
    cmd: str,
    /,
    *,
    direnv: bool = False,
    env: Mapping[str, str | None] | None = None,
    cwd: PathLike | None = None,
    input_: str | None = None,
    skip_log: bool = False,
) -> str:
    if is_root():
        cmd = cmd.replace("sudo ", "")
    desc = f"Running {cmd!r}"
    if direnv:
        desc = f"{desc} [direnv]"
        cmd = f"{SOURCE_BASHRC}; {EVAL_DIRENV_EXPORT}; {cmd}"
    if env is not None:
        desc = f"{desc} [env={env}]"
    if cwd is not None:
        desc = f"{desc} [cwd={cwd}]"
    if not skip_log:
        _LOGGER.info("%s...", desc)
    with temp_environ(env):
        return check_output(
            cmd, executable=which("bash"), shell=True, cwd=cwd, input=input_, text=True
        ).rstrip("\n")


def run_commands(
    *cmds: str,
    direnv: bool = False,
    env: Mapping[str, str | None] | None = None,
    cwd: PathLike | None = None,
    input_: str | None = None,
    skip_log: bool = False,
) -> list[str]:
    return [
        run_command(
            cmd, direnv=direnv, env=env, cwd=cwd, input_=input_, skip_log=skip_log
        )
        for cmd in cmds
    ]


def symlink(
    path_from: PathLike, path_to: PathLike, /, *, skip_log: bool = False
) -> None:
    path_from, path_to = map(full_path, [path_from, path_to])
    is_symlink = path_from.is_symlink()
    resolved = path_from.resolve()
    res_exists_and_correct = resolved.exists() and (resolved == path_to.resolve())
    if is_symlink and res_exists_and_correct:
        return
    if (is_symlink and not res_exists_and_correct) or path_from.exists():
        _ = run_command(f"sudo unlink {path_from}", skip_log=skip_log)
    path_from.parent.mkdir(parents=True, exist_ok=True)
    _ = run_command(f"ln -s {path_to} {path_from}", skip_log=skip_log)


@contextmanager
def temp_environ(env: Mapping[str, str | None] | None = None, /) -> Iterator[None]:
    if env is None:
        yield
        return

    prev = {key: getenv(key) for key in env}

    def apply(mapping: Mapping[str, str | None], /) -> None:
        for key, value in mapping.items():
            if value is None:
                with suppress(KeyError):
                    del environ[key]
            else:
                environ[key] = value

    apply(env)
    try:
        yield
    finally:
        apply(prev)


class TemporaryDirectory:
    def __init__(self) -> None:
        super().__init__()
        self._temp_dir = tempfile.TemporaryDirectory()
        self.path = Path(self._temp_dir.name)

    def __enter__(self) -> Path:
        return Path(self._temp_dir.__enter__())

    def __exit__(
        self,
        exc: type[BaseException] | None,
        val: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self._temp_dir.__exit__(exc, val, tb)


def touch(path: PathLike, /) -> None:
    path = full_path(path)
    if path.exists():
        _LOGGER.debug("%r already exists")
        return
    _LOGGER.debug("Touching %r...", str(path))
    _ = run_commands(f"sudo mkdir -p {path}", f"sudo touch {path}")


def update_submodules(
    *, cwd: PathLike | None = None, version: str | None = None
) -> None:
    _LOGGER.info("Updating submodules...")
    _ = run_commands(
        "git submodule update --init --recursive",
        "git submodule foreach --recursive 'git checkout --force $(git symbolic-ref refs/remotes/origin/HEAD --short | sed ''s#origin/##'') && git pull --ff-only --force --prune --tags'",
        cwd=cwd,
    )
    if version is not None:
        _ = run_command(f"git checkout {version}", cwd=cwd)


def uv_tool_install(tool: str, /) -> None:
    if have_command(tool):
        return
    _LOGGER.info("Installing %r...", tool)
    _ = run_command(f"uv tool install {tool}")


def which(cmd: str, /) -> Path | None:
    result = shutil.which(cmd)
    return None if result is None else full_path(result)


def write_template(
    path_from: PathLike,
    path_to: PathLike,
    /,
    *,
    skip_log: bool = False,
    executable: bool = False,
    immutable: bool = False,
    ownership: bool = False,
    **kwargs: Any,
) -> None:
    path_from = full_path(path_from)
    text = Template(path_from.read_text()).substitute(**kwargs)
    write_text(
        text,
        path_to,
        skip_log=skip_log,
        executable=executable,
        immutable=immutable,
        ownership=ownership,
    )


def write_text(
    text: str,
    path: PathLike,
    /,
    *,
    skip_log: bool = False,
    executable: bool = False,
    immutable: bool = False,
    ownership: bool = False,
) -> None:
    path_to = full_path(path)
    if path_to.exists() and (path_to.read_text() == text):
        return
    if not skip_log:
        lines = text.splitlines()
        desc = "\n".join(lines[:3]) + "..." if len(lines) >= 3 else text
        _LOGGER.info("Writing %r to %r...", desc, str(path))
    with TemporaryDirectory() as temp_dir:
        path_from = temp_dir / path_to.name
        _ = path_from.write_text(text)
        cp(
            path_from,
            path_to,
            skip_log=True,
            executable=executable,
            immutable=immutable,
            ownership=ownership,
        )


@contextmanager
def yield_download(url: str, /) -> Iterator[Path]:
    _LOGGER.info("Yielding download of %r...", url)
    filename = full_path(urlparse(url).path).name
    with TemporaryDirectory() as temp_dir:
        temp_file = temp_dir / filename
        download(url, temp_file)
        yield temp_file


@contextmanager
def yield_github_latest_download(
    owner: str, repo: str, filename_template: str, /
) -> Iterator[Path]:
    tag = get_latest_tag(owner, repo)
    filename = Template(filename_template).substitute(tag=tag)
    url = f"https://github.com/{owner}/{repo}/releases/download/{tag}/{filename}"
    with yield_download(url) as temp_file:
        yield temp_file


@contextmanager
def yield_tar_gz_contents(path: Path, /) -> Iterator[Path]:
    with tarfile.open(path, mode="r:gz") as tf, TemporaryDirectory() as temp_dir:
        _ = tf.extractall(path=temp_dir)
        yield Path(temp_dir)


__all__ = [
    "EVAL_DIRENV_EXPORT",
    "SOURCE_BASHRC",
    "TemporaryDirectory",
    "append_contents",
    "apt_install",
    "apt_update",
    "brew_install",
    "brew_installed",
    "check_for_commands",
    "chmod",
    "chown",
    "contains_line",
    "cp",
    "download",
    "dpkg_install",
    "full_path",
    "get_latest_tag",
    "git_pull",
    "have_command",
    "is_root",
    "luarocks_install",
    "mac_app_exists",
    "replace_line",
    "replace_lines",
    "rm",
    "run_command",
    "run_commands",
    "symlink",
    "temp_environ",
    "touch",
    "update_submodules",
    "uv_tool_install",
    "which",
    "write_template",
    "write_text",
    "yield_download",
    "yield_github_latest_download",
    "yield_tar_gz_contents",
]
