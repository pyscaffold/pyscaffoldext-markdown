# Changelog

<!-- ## Version 0.5.1 (development) -->

## Version 0.5

* Switch to [`myst-parser`](https://pypi.org/project/myst-parser/) from `recommonmark`, PR #16
* Added badges to the `README.md` template, PR #21
* Remove description section in `README.md`, PR #39
* Add a static `CONTRIBUTING.md` template, PR #27

## Version 0.4.1

- Latest updates from PyScaffold
- Fix issue with kebab-cased-keys in `setup.cfg`, PR #13
- Fix issue of dsproject extension `KeyError: 'long-description'`, issue #20

## Version 0.4

- Changes required for PyScaffold v4.0
- Updated system tests/CI using `pyscaffoldext-custom-extension`
- Simplified templates package thanks to `pyscaffold.templates.get_template`
- Removed unnecessary `coding: utf-8` comments
- Use symlinks to load `README.md`, `AUTHORS.md`, `CHANGELOG.md` into Sphinx, issues #6, #7.

## Version 0.3.2

- Fix wrong `long-description` in `setup.cfg`
- Remove deprecated `enable_auto_doc_ref` option
- Remove deprecated `source_parsers`

## Version 0.3.1

- Some cosmetics

## Version 0.3

- Changes necessary for PyScaffold 3.2
- Regenerated extension using `--custom-extension`
- Several cleanups

## Version 0.2.1

- Fix windows error

## Version 0.2

- Use `helpers.modify` where appropriate

## Version 0.1

- Initial release
