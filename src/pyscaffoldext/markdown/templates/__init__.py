# -*- coding: utf-8 -*-
"""
Templates for all files this extension provides
"""
import os.path
import string
from pkgutil import get_data


def get_template(name):
    """Retrieve the template by name

    Args:
        name: name of template without suffix

    Returns:
        :obj:`string.Template`: template
    """
    namespace, pkg_name = __name__.split(".")[:2]
    file_name = "{name}.template".format(name=name)
    data = get_data(namespace, os.path.join(pkg_name, "templates", file_name))
    return string.Template(data.decode(encoding='utf8'))


def readme(opts):
    """Template of README.md

    Args:
        opts: mapping parameters as dictionary

    Returns:
        str: file content as string
    """
    template = get_template("readme")
    return template.substitute(opts)


def authors(opts):
    """Template of AUTHORS.md

    Args:
        opts: mapping parameters as dictionary

    Returns:
        str: file content as string
    """
    template = get_template("authors")
    return template.substitute(opts)


def changelog(opts):
    """Template of CHANGELOG.md

    Args:
        opts: mapping parameters as dictionary

    Returns:
        str: file content as string
    """
    template = get_template("changelog")
    return template.substitute(opts)
