# -*- coding: utf-8 -*-
"""
Templates for all files this extension provides
"""
from pyscaffold.templates import get_template


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
