# -*- coding: utf-8 -*-
"""
Implementation of a simple extension that additionally
adds the file pyproject.toml
"""
from pyscaffold.api import Extension
from pyscaffold.api import helpers

from .templates import pyproject_toml

__author__ = "Florian Wilhelm"
__copyright__ = "Florian Wilhelm"
__license__ = "mit"


# ToDo: Write actual logic
# ToDo: Add long_description_content_type = text/markdown to setup.cfg
class Markdown(Extension):
    """Replace reStructuredText by Markdown"""
    def activate(self, actions):
        """Activate extension

        Args:
            actions (list): list of actions to perform

        Returns:
            list: updated list of actions
        """
        return self.register(
            actions,
            self.add_pyproject_toml,
            after='define_structure')

    def add_pyproject_toml(self, struct, opts):
        """Add the pyproject.toml file

        Args:
            struct (dict): project representation as (possibly) nested
                :obj:`dict`.
            opts (dict): given options, see :obj:`create_project` for
                an extensive list.

        Returns:
            struct, opts: updated project representation and options
        """
        file = [opts['project'], 'pyproject.toml']
        content = pyproject_toml(opts)
        struct = helpers.ensure(struct, file, content)
        return struct, opts
