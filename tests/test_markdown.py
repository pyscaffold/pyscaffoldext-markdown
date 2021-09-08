from configparser import ConfigParser
from textwrap import dedent

import pytest
from pyscaffold import __version__ as pyscaffold_version
from pyscaffold import api, cli

from pyscaffoldext.markdown.extension import DOC_REQUIREMENTS, Markdown, add_long_desc

CONV_FILES = [
    "README",
    "AUTHORS",
    "CHANGELOG",
    "CONTRIBUTING" "docs/index",
    "docs/readme",
    "docs/authors",
    "docs/changelog",
    "docs/contributing",
]


def test_underscore_keys():
    # Dash-separated keys for setup.cfg were deprecated by setuptools, so it is good to
    # ensure they don't occur
    examples = [
        """\
        [metadata]
        long-description: a-pkg
        long-description-content-type: text/x-rst
        """,
        """\
        [metadata]
        long_description: a-pkg
        long_description_content_type: text/x-rst
        """,
        """\
        [metadata]
        long-description: a-pkg
        """,
        """\
        [metadata]
        long_description: a-pkg
        """,
    ]

    for example in examples:
        modified = add_long_desc(dedent(example))
        cfg = ConfigParser()
        cfg.read_string(modified)
        options = list(cfg["metadata"].keys())
        print(modified)
        assert "long_description" in options
        assert "long_description_content_type" in options
        assert "long-description" not in options
        assert "long-description-content-type" not in options


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
    assert "text/markdown" in str(cfg["metadata"]["long_description_content_type"])
    assert "file: README" in str(cfg["metadata"]["long_description"])

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
