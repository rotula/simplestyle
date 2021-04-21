#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
All classes and helpers dealing with styles
"""

import sys
if sys.version_info.major >= 3:
    PY3 = True
    unicode = str
else:
    PY3 = False

from .css import SimpleCSSParser, CSSEmptyDocumentError

class StyleError(Exception): pass
class EmptyStyleError(StyleError): pass

class Style(object):
    """Represents one style"""

    fontname = None
    size = -1
    valign = None
    bold = False
    italics = False
    smallcaps = False

    _size_tolerance = 0.0  # size tolerance as factor

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k == "fontname":
                self.fontname = v
            elif k == "size":
                self.size = float(v)
            elif k == "valign":
                self.valign = v
            elif k == "bold":
                self.bold = True if v else False
            elif k == "italics":
                self.italics = True if v else False
            elif k == "smallcaps":
                self.smallcaps = True if v else False
            else:
                raise StyleError("Unsupported style: {}".format(k))

    def set_size_tolerance(self, tolerance):
        """
        Set a size tolerance for comparing font sizes.

        Args:
            tolerance (float): Factor to set the tolerance of size
                equality. A size will compare equal to the size of
                the current style, if
                size*(1-tolerance) <= compare_size <= size*(1+tolerance).
                The default value is 0.0.
        """
        self._size_tolerance = tolerance

    def __eq__(self, other):
        """Override equals operator"""
        if not isinstance(other, self.__class__):
            return False
        if self.fontname != other.fontname:
            return False
        # if self.size != other.size:
        #    return False
        if not (self._equal_size(self.size, other.size)):
            return False
        if self.valign != other.valign:
            return False
        if self.bold != other.bold:
            return False
        if self.italics != other.italics:
            return False
        if self.smallcaps != other.smallcaps:
            return False
        return True

    def _equal_size(self, s1, s2):
        if s1 > s2:
            low = s1 - s1*self._size_tolerance
            high = s1 + s1*self._size_tolerance
            return low <= s2 <= high
        else:
            low = s2 - s2*self._size_tolerance
            high = s2 + s2*self._size_tolerance
            return low <= s1 <= high

    def __ne__(self, other):
        """Override not equals operator"""
        return not self.__eq__(other)

    def __repr__(self):
        ret = u"Style("
        stmts = []
        if self.fontname:
            stmts.append(unicode(self.fontname))
        if self.size != -1:
            stmts.append(unicode("{}pt".format(self.size)))
        if self.valign:
            stmts.append(unicode(self.valign))
        if self.bold:
            stmts.append(u"bold")
        if self.italics:
            stmts.append(u"italics")
        if self.smallcaps:
            stmts.append(u"smallcaps")
        ret += u" ".join(stmts)
        ret += u")"
        return ret

    def reset(self):
        """Reset values to defaults"""
        self.fontname = None
        self.size = -1
        self.valign = None
        self.bold = False
        self.italics = False
        self.smallcaps = False

    def get_css(self):
        """Output as CSS"""
        statements = []
        if self.fontname:
            statements.append("font-family: \"{}\"".format(self.fontname))
        if self.size != -1:
            statements.append("font-size: {}pt".format(self.size))
        if self.valign:
            statements.append("vertical-align: {}".format(self.valign))
        if self.bold:
            statements.append("font-weight: bold")
        if self.italics:
            statements.append("font-style: italic")
        if self.smallcaps:
            statements.append("font-variant: small-caps")
        return "; ".join(statements)

    def from_css(self, css, merge=False):
        """Parse simple CSS declarations and extract supported styles
        
        Args:
            css (str): the CSS declarations suite to parse
            merge (bool): if false, set back all styles to defaults
                (usually None), defaults to False

        Note: Unsupported properties are being discarded silently.
        """
        try:
            decls = SimpleCSSParser(css).parse()
        except CSSEmptyDocumentError:
            return
        if not merge:
            self.reset()
        for prop, expr in decls:
            if prop == "font-family":
                self.fontname = expr
            elif prop == "font-size":
                if not expr.endswith("pt"):
                    raise StyleError("Other units for font-size than "\
                            "points (pt) not supported.")
                expr = expr[0:expr.find("pt")].strip()
                self.size = float(expr)
            elif prop == "vertical-align":
                self.valign = expr
            elif prop == "font-weight":
                if expr == "bold":
                    self.bold = True
            elif prop == "font-style":
                if expr == "italic":
                    self.italics = True
            elif prop == "font-variant":
                if expr == "small-caps":
                    self.smallcaps = True
