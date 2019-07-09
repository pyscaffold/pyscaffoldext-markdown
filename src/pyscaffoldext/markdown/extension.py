# -*- coding: utf-8 -*-
"""
Extensions that replaces reStructuredText by Markdown
"""
import re

from pyscaffold.api import Extension
from pyscaffold.api import helpers
from pyscaffold.contrib.configupdater import ConfigUpdater

from .templates import readme  # , authors, changelog

__author__ = "Florian Wilhelm"
__copyright__ = "Florian Wilhelm"
__license__ = "mit"


AUTO_STRUCTIFY_CONF = """
# To configure AutoStructify
def setup(app):
    from recommonmark.transform import AutoStructify
    app.add_config_value('recommonmark_config', {
        'auto_toc_tree_section': 'Contents',
        'enable_eval_rst': True,
        'enable_math': True,
        'enable_inline_math': True
    }, True)
    app.add_transform(AutoStructify)
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
            before='verify_project_dir')

    @staticmethod
    def add_long_desc(content):
        updater = ConfigUpdater()
        updater.read_string(content)
        metadata = updater['metadata']
        long_desc_type = 'long-description-content-type'
        if long_desc_type not in metadata:
            (metadata['long-description'].add_after
                .option(long_desc_type, 'text/markdown'))
        return str(updater)

    @staticmethod
    def add_sphinx_md(content):
        content = content.splitlines()
        # add AutoStructify configuration
        idx = [i for i, line in enumerate(content)
               if line.startswith('source_suffix =')][0]
        content[idx] = "source_suffix = ['.rst', '.md']"
        content.insert(idx - 1, AUTO_STRUCTIFY_CONF)
        # add recommonmark extension
        ext_start = [i for i, line in enumerate(content)
                     if line.startswith('extensions =')][0]
        idx = [i for i, line in enumerate(content[ext_start:])
               if line.endswith("']")][0]
        content.insert(ext_start + idx + 1,
                       "extensions.append('recommonmark')")
        return '\n'.join(content)

    @staticmethod
    def rst2md(x):
        """Convert include file from rst to md

        Args:
            x (str): content of rst file

        Returns:
            str: content of rst file
        """
        return re.sub(r'(\.\. include:: \.\..+)\.(rst)', r'\1.md', x)

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

        file_path = [opts['project'], 'setup.cfg']
        struct = helpers.modify(struct, file_path, self.add_long_desc)

        # use when docutils issue is fixed, see #1
        # for file in ('authors.rst', 'changelog.rst'):
        #    file_path = [opts['project'], 'docs', file]
        #    struct = helpers.modify(struct, file_path, self.rst2md)
        file_path = [opts['project'], 'docs', 'conf.py']
        struct = helpers.modify(struct, file_path, self.add_sphinx_md)

        return struct, opts
