"""Extension that replaces reStructuredText by Markdown"""
import re
from functools import partial
from typing import List

from configupdater import ConfigUpdater
from pyscaffold.actions import Action, ActionParams, ScaffoldOpts, Structure
from pyscaffold.extensions import Extension
from pyscaffold.operations import no_overwrite
from pyscaffold.structure import merge, reify_content, resolve_leaf
from pyscaffold.templates import get_template

from . import templates

__author__ = "Florian Wilhelm"
__copyright__ = "Florian Wilhelm"
__license__ = "MIT"


AUTO_STRUCTIFY_CONF = """
# To configure AutoStructify
def setup(app):
    from recommonmark.transform import AutoStructify

    params = {
        "auto_toc_tree_section": "Contents",
        "enable_eval_rst": True,
        "enable_auto_doc_ref": True,
        "enable_math": True,
        "enable_inline_math": True,
    }
    app.add_config_value("recommonmark_config", params, True)
    app.add_transform(AutoStructify)
"""

CONV_FILES = {
    "README": "readme",
    # Use when docutils issue is fixed, see #1
    # "AUTHORS": "authors",
    # "CHANGELOG": "changelog"
}

DOC_REQUIREMENTS = ["recommonmark"]

template = partial(get_template, relative_to=templates)


class Markdown(Extension):
    """Replace reStructuredText by Markdown"""

    def activate(self, actions: List[Action]) -> List[Action]:
        """Activate extension. See :obj:`pyscaffold.extension.Extension.activate`."""
        actions = self.register(actions, add_doc_requirements)
        return self.register(actions, convert_files, before="verify_project_dir")


def add_long_desc(content: str) -> str:
    updater = ConfigUpdater()
    updater.read_string(content)
    metadata = updater["metadata"]
    metadata["long-description"].value = "file: README.md"
    long_desc_type = "long-description-content-type"
    long_desc_value = "text/markdown; charset=UTF-8; variant=GFM"
    if long_desc_type not in metadata:
        metadata["long-description"].add_after.option(long_desc_type, long_desc_value)
    else:
        metadata[long_desc_type].value = long_desc_value
    return str(updater)


def add_sphinx_md(original: str) -> str:
    content = original.splitlines()
    # add AutoStructify configuration
    j = next(i for i, line in enumerate(content) if line.startswith("source_suffix ="))
    content[j] = "source_suffix = ['.rst', '.md']"
    content.insert(j - 1, AUTO_STRUCTIFY_CONF)
    # add recommonmark extension
    start = next(i for i, line in enumerate(content) if line.startswith("extensions ="))
    j = next(i for i, line in enumerate(content[start:]) if line.endswith("']"))
    content.insert(start + j + 1, "extensions.append('recommonmark')")
    return "\n".join(content)


def add_doc_requirements(struct: Structure, opts: ScaffoldOpts) -> ActionParams:
    """In order to build the docs new requirements are necessary now.

    This action will make sure ``tox -e docs`` run without problems.
    """

    files: Structure = {
        "docs": {
            "requirements.txt": ("\n".join(DOC_REQUIREMENTS) + "\n", no_overwrite())
        }
    }

    original, file_op = resolve_leaf(struct.get("tox.ini"))
    original = reify_content(original, opts)
    if original:
        content = original.splitlines()
        j = next(i for i, line in enumerate(content) if "docs/requirements.txt" in line)
        content[j] = "    -r docs/requirements.txt"
        if content[-1]:
            content.append("")  # ensure empty line at the end (pre-commit)
        files["tox.ini"] = ("\n".join(content), file_op)

    return merge(struct, files), opts


def rst2md(content: str) -> str:
    """Convert include file from rst to md

    Args:
        content: content of rst file

    Returns:
        content of md file
    """
    return re.sub(r"(\.\. include:: \.\..+)\.(rst)", r"\1.md", content)


def convert_files(struct: Structure, opts: ScaffoldOpts) -> ActionParams:
    """Convert all rst files to proper md and activate Sphinx md.
    See :obj:`pyscaffold.actions.Action`
    """
    if opts["update"] and not opts["force"]:
        return struct, opts

    struct = struct.copy()
    for file, template_name in CONV_FILES.items():
        # remove rst file
        _, file_op = resolve_leaf(struct.pop(f"{file}.rst"))
        # add md file
        struct[f"{file}.md"] = (template(template_name), file_op)

    content, file_op = resolve_leaf(struct["setup.cfg"])
    struct["setup.cfg"] = (add_long_desc(reify_content(content, opts)), file_op)

    # use when docutils issue is fixed, see #1
    # for file in ("authors", "changelog"):
    #     content, file_op = resolve_leaf(struct["docs"].pop(f"{file}.rst"))
    #     struct["docs"][f"{file}.md"] = (rst2md(reify_content(content, opts)), file_op)

    content, file_op = resolve_leaf(struct["docs"]["conf.py"])
    struct["docs"]["conf.py"] = (add_sphinx_md(reify_content(content, opts)), file_op)

    return struct, opts
