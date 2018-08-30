# -*- coding: utf-8 -*-
"""
Extensions that replaces reStructuredText by Markdown
"""
import os
import re

from pyscaffold.api import Extension
from pyscaffold.api import helpers
from pyscaffold.contrib.configupdater import ConfigUpdater

from .templates import readme, authors, changelog

__author__ = "Florian Wilhelm"
__copyright__ = "Florian Wilhelm"
__license__ = "mit"


SRC_PARSERS = """
# To configure AutoStructify
def setup(app):
    from recommonmark.transform import AutoStructify
    app.add_config_value('recommonmark_config', {
        'auto_toc_tree_section': 'Contents',
        'enable_eval_rst': True,
        'enable_auto_doc_ref': True,
        'enable_math': True,
        'enable_inline_math': True
    }, True)
    app.add_transform(AutoStructify)
    
# Additional parsers besides rst
source_parsers = {
   '.md': 'recommonmark.parser.CommonMarkParser',
}
"""


class MarkDown(Extension):
    """Replace reStructuredText by Markdown"""
    CONV_FILES = {"README": readme,
                  # Use when docutils issue is fixed, see #1
                  # "AUTHORS": authors,
                  # "CHANGELOG": changelog
                  }

    def activate(self, actions):
        """Activate extension

        Args:
            actions (list): list of actions to perform

        Returns:
            list: updated list of actions
        """
        return self.register(
            actions,
            self.markdown,
            after='define_structure')

    def add_long_desc(self, content):
        updater = ConfigUpdater()
        updater.read_string(content)
        (updater['metadata']['long-description'].add_after
            .option('long-description-content-type', 'text/markdown'))
        return str(updater)

    def add_sphinx_md(self, content):
        content = content.split(os.linesep)
        idx = [i for i, line in enumerate(content)
               if line.startswith('source_suffix =')][0]
        content[idx] = "source_suffix = ['.rst', '.md']"
        content.insert(idx-1, SRC_PARSERS)
        return os.linesep.join(content)

    def markdown(self, struct, opts):
        """Convert all rst files to proper md and activate Sphinx md

        Args:
            struct (dict): project representation as (possibly) nested
                :obj:`dict`.
            opts (dict): given options, see :obj:`create_project` for
                an extensive list.

        Returns:
            struct, opts: updated project representation and options
        """
        if opts['update'] and not opts['force']:
            return struct, opts
        for file, template in self.CONV_FILES.items():
            # remove rst file
            file_path = [opts['project'], "{}.rst".format(file)]
            struct = helpers.reject(struct, file_path)
            # add md file
            file_path = [opts['project'], "{}.md".format(file)]
            struct = helpers.ensure(struct, file_path, template(opts))

        root = struct[opts['project']]
        root['setup.cfg'] = mod_content(root['setup.cfg'], self.add_long_desc)

        docs = root['docs']
        # use when docutils issue is fixed, see #1
        # for file in ('authors.rst', 'changelog.rst'):
        #    docs[file] = mod_content(docs[file], rst2md)
        docs['conf.py'] = self.add_sphinx_md(docs['conf.py'])

        return struct, opts


def mod_content(value, func):
    """Modifies content of structure value
    Args:
        value: tuple or str from project structure

    Returns:
        tuple or str for project structure
    """
    if isinstance(value, (tuple, list)):
        content, rule = value
    else:
        content, rule = value, None
    return func(content), rule


def rst2md(x):
    """Convert include file from rst to md

    Args:
        x (str): content of rst file

    Returns:
        str: content of rst file
    """
    return re.sub(r'(\.\. include:: \.\..+)\.(rst)', r'\1.md', x)
