import os
import sys
from contextlib import contextmanager
from pathlib import Path

import pytest

from fetchbin.console import GuessProjectNameError, guess_bin_path, guess_project_name


@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


@pytest.mark.parametrize(
    "fixture_dir,expected",
    [
        ("tests/fixtures/a/", "project"),
        ("tests/fixtures/c/", "bin/project"),
        ("tests/fixtures/d/", "bin/project"),
        ("tests/fixtures/e/", "project/project"),
        ("tests/fixtures/g/", "project-v0.0.0/project"),
        ("tests/fixtures/h/", "bin/project"),
        ("tests/fixtures/i/", "project-v0.0.0/bin/project"),
        ("tests/fixtures/k/", "project-0.0.0/project"),
        ("tests/fixtures/l/", "project-0.0.0/bin/project"),
    ],
)
def test_guess_bin_path(fixture_dir, expected):
    with cd(fixture_dir):
        assert guess_bin_path("project") == Path(expected)


@pytest.mark.parametrize(
    "fixture_dir,expected",
    [
        ("tests/fixtures/n/", "project-darwin-amd64"),
        ("tests/fixtures/o/", "project-darwin-amd64"),
        ("tests/fixtures/p/", "project-v0.0.0-darwin"),
        ("tests/fixtures/q/", "project-0.0.0-darwin"),
    ],
)
@pytest.mark.skipif(sys.platform != "darwin", reason="Mac specific tests")
def test_guess_bin_path_macos(fixture_dir, expected):
    with cd(fixture_dir):
        assert guess_bin_path("project") == Path(expected)


@pytest.mark.parametrize(
    "fixture_dir,expected",
    [
        ("tests/fixtures/b/", "project-linux-amd64"),
        ("tests/fixtures/f/", "project-linux-amd64"),
        ("tests/fixtures/j/", "project-v0.0.0-linux"),
        ("tests/fixtures/m/", "project-0.0.0-linux"),
    ],
)
@pytest.mark.skipif(sys.platform != "linux", reason="Linux specific tests")
def test_guess_bin_path_linux(fixture_dir, expected):
    with cd(fixture_dir):
        assert guess_bin_path("project") == Path(expected)


@pytest.mark.parametrize(
    "fixture_dir",
    [
        ("tests/fixtures/not-found-a/"),
        ("tests/fixtures/not-found-b/"),
    ],
)
def test_guess_bin_path_not_found(fixture_dir):
    with pytest.raises(FileNotFoundError):
        with cd(fixture_dir):
            guess_bin_path("project")


@pytest.mark.parametrize(
    "url",
    [
        "http://github.com/someuser/somename/release/0.0.0/anothername.tar.gz",
        "https://github.com/someuser/somename/release/0.0.0/",
        "github.com/someuser/somename/release/0.0.0/",
        "someuser/somename/release/0.0.0/",
        "someuser/somename",
    ],
)
def test_guess_project_name(url):
    assert guess_project_name(url) == "somename"


def test_guess_project_name_raises_error():
    with pytest.raises(GuessProjectNameError):
        guess_project_name("")
