import sys
from pathlib import Path

import pytest
from pyscaffold import cli
from pyscaffold.file_system import chdir

from pyscaffoldext.markdown.extension import Markdown

from .helpers import run_common_tasks

EXT_FLAGS = [Markdown().flag]

# If you need to check logs with caplog, have a look on
# pyscaffoldext-custom-extension's tests/conftest.py file and the
# `isolated_logger` fixture.


def test_add_custom_extension(tmpfolder):
    args = ["my_project", "--no-config", "-p", "my_package", *EXT_FLAGS]
    # --no-config: avoid extra config from dev's machine interference
    cli.main(args)
    assert Path("my_project/src/my_package/__init__.py").exists()
    assert Path("my_project/README.md").exists()
    assert not Path("my_project/README.rst").exists()


def test_add_custom_extension_and_pretend(tmpfolder):
    args = ["my_project", "--no-config", "--pretend", "-p", "my_package", *EXT_FLAGS]
    # --no-config: avoid extra config from dev's machine interference
    cli.main(args)

    assert not Path("my_project/README.md").exists()
    assert not Path("my_project").exists()


def test_add_custom_extension_with_namespace(tmpfolder):
    args = [
        "my_project",
        "--no-config",  # avoid extra config from dev's machine interference
        "--package",
        "my_package",
        "--namespace",
        "my.ns",
        *EXT_FLAGS,
    ]
    cli.main(args)

    assert Path("my_project/src/my/ns/my_package/__init__.py").exists()


@pytest.mark.slow
@pytest.mark.system
def test_generated_extension(tmpfolder):
    use_pre_commit = ["--pre-commit"] if sys.version_info >= (3, 7) else []

    args = [
        "my_project",
        "--no-config",  # avoid extra config from dev's machine interference
        "--venv",  # generate a venv so we can install the resulting project
        *use_pre_commit,  # ensure generated files respect repository conventions
        "--namespace",  # it is very easy to forget users might want to use namespaces
        "my.ns",  # ... so we automatically test the worst case scenario
        *EXT_FLAGS,
    ]
    cli.main(args)

    with chdir("my_project"):
        # Testing a project generated by the custom extension
        run_common_tasks(pre_commit=bool(use_pre_commit))
