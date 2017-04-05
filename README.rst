***********
simplestyle
***********

This package was originally part of a Python tool to extract text data
from PDFs into TEI XML. Some of the style information that was extracted
from the PDF had to be recorded in the resulting TEI file. Among these
were fontname, fontsize, italics, boldface, superscript, subscript.
These were included as simple CSS statements into the ``tagsDecl`` of
the TEI document.

Later it seemed approporiate to remove this very simple style library
from the PDF extraction package and offer it as a little standalone
package, which can be useful in different contexts.

NB: This package might be useful for some people, hence it is published
as an open source package, but it is still very much tailored to some
very special needs for text processing. It is not very likely that this
package will be developed into a general CSS library. If you need this,
you will find plenty of helpful libraries on PyPI.

Download, Installation
======================

simplestyle is available on PyPI
<https://pypi.python.org/pypi/simplestyle>.

Install with ``pip install simplestyle``.

The source code is on GitHub: <https://github.com/rotula/simplestyle>.

Simplified CSS
==============

The simplified CSS grammar understood by this package is as follows::

    css := declaration (";" declaration)* ';'?
    declaration := property ":" expr
    property := [a-zA-Z-]+
    expr := (string | [^;"']+)
    string := string1 | string2
    string1 := "'" [^'\n\r\f] "'"
    string2 := '"' [^"\n\r\f] '"'

Usage
=====

.. code:: pycon

    >>> from simplestyle import Style
    >>> css = "font-size: 10pt"
    >>> style = Style()
    >>> style.from_css(css)
    >>> style.size
    10.0
    >>> style.get_css()
    'font-size: 10.0pt'
    >>> style.italics
    False
    >>> style.from_css("font-style:italic", merge=True)
    >>> style.italics
    True
    >>> style.size
    10.0
    >>> style.get_css()
    'font-size: 10.0pt; font-style: italic'
    >>> style.reset()
    >>> style.get_css()
    ''

