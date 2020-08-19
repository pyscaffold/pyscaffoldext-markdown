[![Build Status](https://api.cirrus-ci.com/github/pyscaffold/pyscaffoldext-markdown.svg?branch=master)](https://cirrus-ci.com/github/pyscaffold/pyscaffoldext-markdown)
[![Coveralls](https://img.shields.io/coveralls/github/pyscaffold/pyscaffoldext-markdown/master.svg)](https://coveralls.io/r/pyscaffold/pyscaffoldext-markdown)
[![PyPI-Server](https://img.shields.io/pypi/v/pyscaffoldext-markdown.svg)](https://pypi.org/project/pyscaffoldext-markdown)

# pyscaffoldext-markdown

PyScaffold extension which replaces [reStructuredText] formatted files
by [Markdown] format except for Sphinx-related files.

## Usage

Just install this package with `pip install pyscaffoldext-markdown`
and note that `putup -h` shows a new option `--markdown`.
Basically this extension will replace `README.rst` by a proper `README.md` and
activate the support of Markdown files in Sphinx.
Due to limitations of the Markdown syntax compared to reStructuredText,
the main documentation files still use reStructuredText by default.

Remember to install [wheel] version 0.31 or higher and use [twine] to upload your
package to [PyPI] instead of `python setup.py release` for this to work, e.g.:
```commandline
python setup.py sdist bdist_wheel
twine upload dist/*
```

<!-- pyscaffold-notes -->

## Making Changes & Contributing

This project uses [pre-commit], please make sure to install it before making any
changes:

```commandline
pip install pre-commit
cd pyscaffoldext-markdown
pre-commit install
```

It is a good idea to update the hooks to the latest version:

```commandline
pre-commit autoupdate
```

Please also check PyScaffold's [contribution guidelines].


## Note

This project has been set up using PyScaffold 3.2. For details and usage
information on PyScaffold see https://pyscaffold.org/.

[reStructuredText]: http://docutils.sourceforge.net/rst.html
[Markdown]: https://daringfireball.net/projects/markdown/
[twine]: https://twine.readthedocs.io/
[PyPI]: https://pypi.org/
[wheel]: https://wheel.readthedocs.io/
[pre-commit]: http://pre-commit.com/
[contribution guidelines]: https://pyscaffold.org/en/latest/contributing.html
