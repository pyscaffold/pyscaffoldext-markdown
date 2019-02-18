# -*- coding: utf-8 -*-
"""
Templates for all files this extension provides
"""
import string
from pkg_resources import resource_string


def get_template(name):
    """Retrieve the template by name

    Args:
        name: name of template

    Returns:
        :obj:`string.Template`: template
    """
    file_name = "{name}.template".format(name=name)
    data = resource_string("pyscaffoldext.markdown.templates",
                           file_name)
    return string.Template(data.decode("UTF-8"))


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
