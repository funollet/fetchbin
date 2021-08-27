import logging
import os
import tempfile
from logging import debug

import click

from . import __version__
from .exceptions import GuessProjectNameError
from .fetch import (
    dest_dir,
    download_file,
    expand,
    guess_bin_path,
    guess_project_name,
    install,
)


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
    logging.basicConfig(level=logging.DEBUG)

    release_url = url
    try:
        name = name or guess_project_name(release_url)
    except GuessProjectNameError:
        raise click.UsageError("Unable to guess the project name. Please use --name")

    with tempfile.TemporaryDirectory() as tmpdirname:
        debug(f"change to directory {tmpdirname}")
        os.chdir(tmpdirname)
        archive = download_file(release_url)
        expand(archive)
        bin_path = guess_bin_path(name)
        install(bin_path, dest_dir() / name)
