import os
import shutil
import tempfile
from pathlib import Path

import click
from requests import get

from . import __version__

DEBUG = False


# Quick and dirty logging.
def debug(s):
    DEBUG and print(f"[debug] {s}")


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


def guess_bin_path(name, base_path):
    """Find the desired executable file using heuristics"""
    candidate = Path(name)
    if candidate.exists():
        return candidate
    raise FileNotFoundError("unable to determine the binary filename")


def install(src, dest):
    """Install binary 'src' in directory 'dest'"""
    dest = dest.expanduser()
    debug(f"install {src} to {dest}")
    shutil.copyfile(src, dest)
    dest.chmod(0o755)


@click.command()
@click.version_option(version=__version__)
@click.argument("url")
@click.option("-n", "--name", type=str)
@click.option("-d", "--dest", type=str, default=dest_dir(), show_default=True)
@click.option("-v", "--verbose", is_flag=True, default=False)
# @click.option('-t', '--tag', type=str)
def main(url, name, dest, verbose):
    """Download and install binary files."""
    # Setup logging.
    global DEBUG
    DEBUG = verbose

    release_url = url
    with tempfile.TemporaryDirectory() as tmpdirname:
        debug(f"change to directory {tmpdirname}")
        os.chdir(tmpdirname)
        archive = download_file(release_url)
        expand(archive)
        bin_path = guess_bin_path(name, archive)
        install(bin_path, dest_dir() / name)