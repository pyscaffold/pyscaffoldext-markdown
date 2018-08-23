pyscaffoldext-markdown
======================

WORK-IN-PROGRESS

PyScaffold extension which replaces [reStructuredText][rst] by [Markdown][md]

Usage
-----

Just install this package with ``pip install pyscaffoldext-markdown``
and note that ``putup -h`` shows a new option ``--markdown``.
Basically this extension will replace all `.rst` files with `.md` files and
Sphinx is configured to use Markdown by default.

Note
----

This project has been set up using PyScaffold 3.1rc1. For details and usage
information on PyScaffold see https://pyscaffold.org/.

[rst]: http://docutils.sourceforge.net/rst.html
[md]: https://daringfireball.net/projects/markdown/
