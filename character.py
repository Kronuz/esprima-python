# -*- coding: utf-8 -*-
# Copyright JS Foundation and other contributors, https://js.foundation/
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import unicode_literals

import sys

import unicodedata
from collections import defaultdict

from .compat import unichr, xrange

# http://stackoverflow.com/questions/14245893/efficiently-list-all-characters-in-a-given-unicode-category
U_CATEGORIES = defaultdict(list)
for c in map(unichr, xrange(sys.maxunicode + 1)):
    U_CATEGORIES[unicodedata.category(c)].append(c)
UNICODE_LETTER = set(
    U_CATEGORIES['Lu'] + U_CATEGORIES['Ll'] +
    U_CATEGORIES['Lt'] + U_CATEGORIES['Lm'] +
    U_CATEGORIES['Lo'] + U_CATEGORIES['Nl']
)
UNICODE_COMBINING_MARK = set(U_CATEGORIES['Mn'] + U_CATEGORIES['Mc'])
UNICODE_DIGIT = set(U_CATEGORIES['Nd'])
UNICODE_CONNECTOR_PUNCTUATION = set(U_CATEGORIES['Pc'])
IDENTIFIER_START = UNICODE_LETTER.union(set(('$', '_', '\\')))
IDENTIFIER_PART = IDENTIFIER_START.union(UNICODE_COMBINING_MARK).union(UNICODE_DIGIT).union(UNICODE_CONNECTOR_PUNCTUATION).union(set((unichr(0x200D), unichr(0x200C))))

WHITE_SPACE = set(map(unichr, (
    0x0009, 0x000B, 0x000C, 0x0020, 0x00A0,
    0x1680, 0x180E, 0x2000, 0x2001, 0x2002,
    0x2003, 0x2004, 0x2005, 0x2006, 0x2007,
    0x2008, 0x2009, 0x200A, 0x202F, 0x205F,
    0x3000, 0xFEFF,
)))
LINE_TERMINATOR = set(map(unichr, (0x000A, 0x000D, 0x2028, 0x2029)))

DECIMAL_CONV = dict((c, n) for n, c in enumerate('0123456789'))
OCTAL_CONV = dict((c, n) for n, c in enumerate('01234567'))
HEX_CONV = dict((c, n) for n, c in enumerate('0123456789abcdef'))
for n, c in enumerate('ABCDEF', 10):
    HEX_CONV[c] = n
DECIMAL_DIGIT = set(DECIMAL_CONV.keys())
OCTAL_DIGIT = set(OCTAL_CONV.keys())
HEX_DIGIT = set(HEX_CONV.keys())


class Character:
    @staticmethod
    def fromCodePoint(code):
        # UTF-16 Encoding
        if (code <= 0xFFFF):
            return unichr(code)
        cu1 = ((code - 0x10000) >> 10) + 0xD800
        cu2 = ((code - 0x10000) & 1023) + 0xDC00
        return unichr(cu1) + unichr(cu2)

    @staticmethod
    def isWhiteSpace(ch):
        return (unichr(ch) if isinstance(ch, int) else ch) in WHITE_SPACE

    @staticmethod
    def isLineTerminator(ch):
        return (unichr(ch) if isinstance(ch, int) else ch) in LINE_TERMINATOR

    @staticmethod
    def isIdentifierStart(ch):
        return (unichr(ch) if isinstance(ch, int) else ch) in IDENTIFIER_START

    @staticmethod
    def isIdentifierPart(ch):
        return (unichr(ch) if isinstance(ch, int) else ch) in IDENTIFIER_PART

    @staticmethod
    def isDecimalDigit(ch):
        return (unichr(ch) if isinstance(ch, int) else ch) in DECIMAL_DIGIT

    @staticmethod
    def isHexDigit(ch):
        return (unichr(ch) if isinstance(ch, int) else ch) in HEX_DIGIT

    @staticmethod
    def isOctalDigit(ch):
        return (unichr(ch) if isinstance(ch, int) else ch) in OCTAL_DIGIT
