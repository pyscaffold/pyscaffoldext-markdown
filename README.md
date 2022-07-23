[![Build Status](https://api.cirrus-ci.com/github/pyscaffold/pyscaffoldext-markdown.svg?branch=master)](https://cirrus-ci.com/github/pyscaffold/pyscaffoldext-markdown)
[![ReadTheDocs](https://readthedocs.org/projects/pyscaffoldext-markdown/badge/?version=latest)](https://pyscaffold.org/projects/markdown/en/latest/)
[![Coveralls](https://img.shields.io/coveralls/github/pyscaffold/pyscaffoldext-markdown/master.svg)](https://coveralls.io/r/pyscaffold/pyscaffoldext-markdown)
[![PyPI-Server](https://img.shields.io/pypi/v/pyscaffoldext-markdown.svg)](https://pypi.org/project/pyscaffoldext-markdown)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/pyscaffoldext-markdown.svg)](https://anaconda.org/conda-forge/pyscaffoldext-markdown)
[![Downloads](https://pepy.tech/badge/pyscaffoldext-markdown/month)](https://pepy.tech/project/pyscaffoldext-markdown)
[![Sponsor](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=ff69b4)](https://github.com/sponsors/FlorianWilhelm)


# pyscaffoldext-markdown

[PyScaffold] extension which replaces [reStructuredText] formatted files
by [Markdown] format (with the help of [MyST]) except for [Sphinx]-related files.


## Usage

Just install this package with either `pip install pyscaffoldext-markdown` or `conda install -c conda-forge pyscaffoldext-markdown`
and note that `putup -h` shows a new option `--markdown`.
Basically this extension will replace `README.rst` by a proper `README.md` and
activate the support of Markdown files in Sphinx.


## Building and Releasing

By default, the [tox] configuration generated by [PyScaffold] is compatible
with Markdown (as implemented in this extension). This means that (after
installing [tox] with [pip] or [pipx]) you can run:

```bash
tox -e docs  # to build your documentation
tox -e build  # to build your package distribution
tox -e publish  # to test your project uploads correctly in test.pypi.org
tox -e publish -- --repository pypi  # to release your package to PyPI
tox -av  # to list all the tasks available
```

Please remember that the command `python setup.py release` is no longer
recommended, so if you don't like [tox], please consider using
[Sphinx] and [twine] directly:

```bash
python -m pip install -U pip setuptools wheel sphinx twine
python setup.py bdist_wheel  # to build your package distributions
make -C docs html  # to build your docs
twine upload dist/*  # to release your package to PyPI
```

<!-- pyscaffold-notes -->

## Making Changes & Contributing

This project uses [pre-commit], please make sure to install it before making any
changes:

```bash
pip install pre-commit
cd pyscaffoldext-markdown
pre-commit install
```

It is a good idea to update the hooks to the latest version:

```bash
pre-commit autoupdate
```

Please also check PyScaffold's [contribution guidelines].


## Note

This project has been set up using PyScaffold 4.0. For details and usage
information on PyScaffold see [https://pyscaffold.org/](https://pyscaffold.org/).

[PyScaffold]: https://pyscaffold.org
[reStructuredText]: https://docutils.sourceforge.io/docs/user/rst/quickstart.html
[Markdown]: https://daringfireball.net/projects/markdown/
[MyST]: https://myst-parser.readthedocs.io/en/latest/index.html
[Sphinx]: https://www.sphinx-doc.org/
[WSL]: https://docs.microsoft.com/en-us/windows/wsl/
[tox]: https://tox.readthedocs.org/
[pip]: https://pip.pypa.io/en/stable/
[pipx]: https://pipxproject.github.io/pipx/
[twine]: https://twine.readthedocs.io/
[PyPI]: https://pypi.org/
[Conda-Forge]: https://anaconda.org/conda-forge/pyscaffoldext-markdown
[pre-commit]: https://pre-commit.com/
[contribution guidelines]: https://pyscaffold.org/en/latest/contributing.html
