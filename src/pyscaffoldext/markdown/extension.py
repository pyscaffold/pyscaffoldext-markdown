"""Extension that replaces reStructuredText by Markdown"""
import os
from functools import partial, reduce
from pathlib import Path
from typing import List

from configupdater import ConfigUpdater
from pyscaffold import file_system as fs
from pyscaffold.actions import Action, ActionParams, ScaffoldOpts, Structure
from pyscaffold.extensions import Extension
from pyscaffold.identification import dasherize
from pyscaffold.log import logger
from pyscaffold.operations import FileContents, FileOp, no_overwrite
from pyscaffold.structure import merge, reify_leaf, reject
from pyscaffold.templates import get_template

from . import templates

__author__ = "Florian Wilhelm"
__copyright__ = "Florian Wilhelm"
__license__ = "MIT"

DESC_KEY = "long_description"
TYPE_KEY = "long_description_content_type"

DOC_REQUIREMENTS = ["recommonmark"]

template = partial(get_template, relative_to=templates)


class Markdown(Extension):
    """Replace reStructuredText by Markdown"""

    def activate(self, actions: List[Action]) -> List[Action]:
        """Activate extension. See :obj:`pyscaffold.extension.Extension.activate`."""
        actions = self.register(actions, add_doc_requirements)
        return self.register(actions, replace_files, before="verify_project_dir")


def add_long_desc(content: str) -> str:
    updater = ConfigUpdater()
    updater.read_string(content)
    metadata = updater["metadata"]

    long_desc = metadata.get(dasherize(DESC_KEY)) or metadata.get(DESC_KEY)
    long_desc.name = DESC_KEY  # dash-separated keys are deprecated in setuptools
    long_desc.value = "file: README.md"
    long_desc_value = "text/markdown; charset=UTF-8; variant=GFM"

    long_desc_type = metadata.get(dasherize(TYPE_KEY)) or metadata.get(TYPE_KEY)
    if long_desc_type:
        long_desc_type.name = TYPE_KEY
        long_desc_type.value = long_desc_value
    else:
        long_desc.add_after.option(TYPE_KEY, long_desc_value)

    return str(updater)


def add_recommonmark(original: str) -> str:
    """Change docs/conf.py to use recommonmark and AutoStructify, enabling md files"""
    content = original.splitlines()
    auto_structify = template("auto_structify").template  # raw string
    recommonmark = '\n# Enable markdown\nextensions.append("recommonmark")\n'
    # add recommonmark extension and AutoStructify configuration
    j = next(i for i, line in enumerate(content) if line.startswith("source_suffix ="))
    content[j] = 'source_suffix = [".rst", ".md"]'
    content.insert(j - 1, auto_structify)
    content.insert(j, recommonmark)
    return "\n".join(content)


def add_doc_requirements(struct: Structure, opts: ScaffoldOpts) -> ActionParams:
    """In order to build the docs new requirements are necessary now.

    The default ``tox.ini`` generated by PyScaffold should already include
    ``-e {toxinidir}/docs/requirements.txt`` in its dependencies. Therefore,
    this action will make sure ``tox -e docs`` run without problems.

    It is important to sort the requirements otherwise pre-commit will raise an error
    for a newly generated file and that would correspond to a bad user experience.
    """
    leaf = struct.get("docs", {}).get("requirements.txt")
    original, file_op = reify_leaf(leaf, opts)
    contents = original or ""

    missing = [req for req in DOC_REQUIREMENTS if req not in contents]
    requirements = [*contents.splitlines(), *missing]

    # It is not trivial to sort the requirements because they include a comment header
    j = (i for (i, line) in enumerate(requirements) if line and not is_commented(line))
    comments_end = next(j, 0)  # first element of the iterator is a non commented line
    comments = requirements[:comments_end]
    sorted_requirements = sorted(requirements[comments_end:])

    new_contents = "\n".join([*comments, *sorted_requirements]) + "\n"
    # ^  pre-commit requires a new line at the end of the file

    files: Structure = {"docs": {"requirements.txt": (new_contents, file_op)}}

    return merge(struct, files), opts


# NOTE: Avoid renaming/removing replace_files.
#       The dsproject extension depends on that name, any changes in the function
#       signature here should be followed by a PR to that repository.
def replace_files(struct: Structure, opts: ScaffoldOpts) -> ActionParams:
    """Replace all rst files to proper md and activate Sphinx md.
    See :obj:`pyscaffold.actions.Action`

    The approach used by recommonmark's own documentation is to include a symbolic link
    file inside the docs directory, instead of trying to do a rst's *include*.

    References:
    - https://github.com/readthedocs/recommonmark/issues/191
    - https://github.com/sphinx-doc/sphinx/issues/701
    - https://github.com/sphinx-doc/sphinx/pull/7739
    """
    # Remove all unnecessary .rst files from struct
    unnecessary = [
        "README.rst",
        "AUTHORS.rst",
        "CHANGELOG.rst",
        "docs/index.rst",
        "docs/readme.rst",
        "docs/authors.rst",
        "docs/changelog.rst",
    ]
    struct = reduce(reject, unnecessary, struct)
    content, file_op = reify_leaf(struct["setup.cfg"], opts)
    struct["setup.cfg"] = (add_long_desc(content), file_op)

    docs = struct.pop("docs", {})  # see comments on ``files``
    content, file_op = reify_leaf(docs["conf.py"], opts)
    root = Path(opts.get("project_path", "."))

    # Define replacement files/links
    files: Structure = {
        "README.md": (template("readme"), no_overwrite()),
        "AUTHORS.md": (template("authors"), no_overwrite()),
        "CHANGELOG.md": (template("changelog"), no_overwrite()),
        "docs": {
            **docs,
            # by popping the docs and merging them back we guarantee the '*.md'
            # files at the root of the repository are processed first, then when it is
            # time to process the `docs` folder, they already exist and can be symlinked
            "conf.py": (add_recommonmark(content), file_op),
            "index.md": (template("index"), no_overwrite()),
            "readme.md": (None, no_overwrite(symlink(root / "README.md"))),
            "authors.md": (None, no_overwrite(symlink(root / "AUTHORS.md"))),
            "changelog.md": (None, no_overwrite(symlink(root / "CHANGELOG.md"))),
        },
    }

    return merge(struct, files), opts


def is_commented(line):
    return line.strip().startswith("#")


def symlink(original_file: fs.PathLike) -> FileOp:
    """Returns a file operation that creates a symlink to ``original_file``."""
    # TODO: Transfer this function to PyScaffold's core (and split it into 2:
    #       a file_system.symlink and an operations.symlink)

    def _symlink(path: Path, _: FileContents, opts: ScaffoldOpts):
        """See ``pyscaffoldext.markdown.extension.symlink``"""
        should_pretend = opts.get("pretend")
        should_log = opts.get("log", should_pretend)
        # ^ When pretending, automatically output logs
        #   (after all, this is the primary purpose of pretending)

        if should_log:
            logger.report("symlink", path, target=original_file)

        if should_pretend:
            return path

        # Since errors in Windows can be tricky, let's print meaningful messages
        if path.exists():
            if opts.get("force"):
                path.unlink()
            else:
                raise FileExistsError(
                    "Impossible to create a symbolic link "
                    f"{{{path} => {original_file}}}.\n{path} already exist.\n"
                )

        if not Path(original_file).exists():
            raise FileNotFoundError(
                "Impossible to create a symbolic link "
                f"{{{path} => {original_file}}}: {original_file} does not exist"
            )

        try:
            # Relative links in Python might be tricky
            # the following implementation is very difficult to be replaced by something
            # completely pathlib-based, see https://bugs.python.org/issue37019
            os.symlink(os.path.relpath(original_file, path.parent), path)
            return path
        except OSError as ex:
            raise SymlinkError(path, original_file) from ex

    return _symlink


class SymlinkError(OSError):
    """\
    Impossible to create a symbolic link {{{link_path} => {original_file}}}.
    If you are using a non-POSIX operating system, please make sure that your user have
    the correct rights and that your system is correctly configured.

    Please check the following references:
    http://github.com/git-for-windows/git/wiki/Symbolic-Links
    https://blogs.windows.com/windowsdeveloper/2016/12/02/symlinks-windows-10/
    https://docs.microsoft.com/en-us/windows/win32/fileio/creating-symbolic-links
    """

    def __init__(self, link_path, original_file, *args, **kwargs):
        docs = self.__class__.__doc__ or ""
        msg = docs.format(original_file=original_file, link_path=link_path)
        super().__init__(msg, *args, **kwargs)
