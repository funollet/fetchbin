import shutil
import sys
from logging import debug
from pathlib import Path

from requests import get

from .exceptions import GuessProjectNameError


def guess_project_name(url):
    try:
        if "github.com/" in url:
            result = url.split("github.com/")[1].split("/")[1]
        else:
            result = url.split("/")[1]
    except IndexError:
        raise GuessProjectNameError("unable to guess the project name")
    debug(f"guess name: {result}")
    return result


def download_file(url, dest_file=""):
    """Download an url into a file"""
    d = Path(dest_file or url.split("/")[-1])
    debug(f"download file {d}")
    with d.open("wb") as download:
        response = get(url)
        download.write(response.content)
    return d


def dest_dir():
    """Return a suitable destination dir for binary files"""
    return Path("~/.local/bin")


def expand(archive):
    """Expand .tgz and .zip, does nothing for other formats"""
    try:
        debug(f"unpack {archive}")
        shutil.unpack_archive(archive)
    except shutil.ReadError:
        debug(f"no need to unpack {archive}")


def guess_bin_path(name):
    """Find the desired executable file using heuristics"""
    candidate = Path(name)
    if candidate.is_file():
        return candidate

    patterns = [
        f"bin/{name}",
        f"**/bin/{name}",
        f"{name}*/{name}",
        f"{name}[_-]{sys.platform}[_-]*",
        f"**/{name}[_-]{sys.platform}[_-]*",
        f"{name}-[0-9].[0-9].[0-9]-{sys.platform}",
        f"{name}-v[0-9].[0-9].[0-9]-{sys.platform}",
    ]
    if sys.platform == "darwin":
        patterns += [
            f"{name}[_-]mac[oO][sS][_-]*",
            f"**/{name}[_-]mac[oO][sS][_-]*",
        ]
    for f in Path(".").glob(f"**/{name}*"):
        for pattern in patterns:
            if f.is_file() and f.match(pattern):
                return f
    raise FileNotFoundError("unable to determine the binary filename")


def install(src, dest):
    """Install binary 'src' in directory 'dest'"""
    dest = dest.expanduser()
    debug(f"install {src} to {dest}")
    shutil.copyfile(src, dest)
    dest.chmod(0o755)
