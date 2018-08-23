# pyscaffoldext-markdown

WORK-IN-PROGRESS

PyScaffold extension which replaces [reStructuredText] by [Markdown]

## Usage

Just install this package with `pip install pyscaffoldext-markdown`
and note that `putup -h` shows a new option `--markdown`.
Basically this extension will replace all `.rst` files with `.md` files and
Sphinx is configured to use Markdown by default.

Remember to install [wheel] version 31 or higher and use [twine] to upload your
package to [PyPI] instead of `python setup.py release` for this to work, i.e.:
```commandline
python setup.py sdist bdist_wheel
twine upload dist/*
```

## Note

This project has been set up using PyScaffold 3.1rc1. For details and usage
information on PyScaffold see https://pyscaffold.org/.

[reStructuredText]: http://docutils.sourceforge.net/rst.html
[Markdown]: https://daringfireball.net/projects/markdown/
[twine]: https://twine.readthedocs.io/
[PyPI]: https://pypi.org/
[wheel]: https://wheel.readthedocs.io/
