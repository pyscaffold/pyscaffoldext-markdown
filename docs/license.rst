..
  Files added to Sphinx' TOC need to have titles, otherwise are ignored.
  Since the license is a .txt file, its title is not parsed/recognised.
  Therefore, we need a new file with a title and the ``include`` directive.
  The ``include`` directive is only available in .rst files.

.. _license:

=======
License
=======

.. include:: ../LICENSE.txt
