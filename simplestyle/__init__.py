# -*- coding: UTF-8 -*-

"""
Handling of simple styles (subset of CSS)
"""

__version__ = "1.2.0"
__all__ = [
        "CSSError",
        "CSSUnexpectedEOFError",
        "CSSMissingSemicolonError",
        "CSSMissingColonError",
        "CSSIllegalCharacterError",
        "CSSEmptyDocumentError",
        "EOF",
        "SimpleCSSParser",
        "StyleError",
        "EmptyStyleError",
        "Style",
    ]

from .css import CSSError
from .css import CSSUnexpectedEOFError
from .css import CSSMissingSemicolonError
from .css import CSSMissingColonError
from .css import CSSIllegalCharacterError
from .css import CSSEmptyDocumentError
from .css import EOF
from .css import SimpleCSSParser

from .styles import StyleError
from .styles import EmptyStyleError
from .styles import Style

