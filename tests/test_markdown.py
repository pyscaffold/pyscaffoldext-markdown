from configparser import ConfigParser

import pytest
from pyscaffold import __version__ as pyscaffold_version
from pyscaffold import api, cli

from pyscaffoldext.markdown.extension import DOC_REQUIREMENTS, Markdown

CONV_FILES = [
    "README",
    "AUTHORS",
    "CHANGELOG",
    "docs/index",
    "docs/readme",
    "docs/authors",
    "docs/changelog",
]


@pytest.mark.slow
def test_create_project_with_markdown(tmpfolder):
    # Given options with the markdown extension,
    opts = dict(
        project_path="proj",
        package="pkg",
        version=pyscaffold_version,
        extensions=[Markdown()],
        config_files=api.NO_CONFIG,
    )
    # NO_CONFIG: avoid extra config from dev's machine interference

    # when the project is created,
    api.create_project(opts)
    assert (tmpfolder / "proj/docs").is_dir()

    # then markdown files should exist,
    for file in CONV_FILES:
        assert (tmpfolder / f"proj/{file}.md").exists()
        assert not (tmpfolder / f"proj/{file}.rst").exists()

    # the content-type of README should be changed accordingly,
    existing_setup = (tmpfolder / "proj/setup.cfg").read_text()
    cfg = ConfigParser()
    cfg.read_string(existing_setup)
    assert "text/markdown" in str(cfg["metadata"]["long-description-content-type"])

    # and new doc requirements should be added to docs/requirements.txt
    requirements_txt = (tmpfolder / "proj/docs/requirements.txt").read_text()
    for req in DOC_REQUIREMENTS:
        assert req in requirements_txt


@pytest.mark.slow
@pytest.mark.system
def test_cli_with_markdown_and_update(tmpfolder):
    # Given a project exists with the markdown extension
    opts = dict(
        project_path="proj",
        package="pkg",
        version=pyscaffold_version,
        extensions=[Markdown()],
        config_files=api.NO_CONFIG,
    )
    api.create_project(opts)

    # when the project is updated
    args = ["--no-config", "--update", "proj"]
    cli.main(args)

    # then markdown files should still exist, and not rst equivalent should be created
    for file in CONV_FILES:
        assert (tmpfolder / f"proj/{file}.md").exists()
        assert not (tmpfolder / f"proj/{file}.rst").exists()
