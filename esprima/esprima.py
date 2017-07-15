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

from __future__ import absolute_import, unicode_literals

from .objects import toDict
from .syntax import Syntax  # NOQA
from .error_handler import Error  # NOQA
from .parser import Parser
from .jsx_parser import JSXParser
from .tokenizer import Tokenizer


def parse(code, options={}, delegate=None):
    if options.get('jsx', False):
        parser = JSXParser(code, options=options, delegate=delegate)
    else:
        parser = Parser(code, options=options, delegate=delegate)

    if options.get('sourceType', 'script') == 'module':
        ast = parser.parseModule()
    else:
        ast = parser.parseScript()

    if parser.config.tokens:
        ast.tokens = parser.tokens

    if parser.config.comment:
        ast.comments = parser.comments

    if parser.config.tolerant:
        ast.errors = parser.errorHandler.errors

    return toDict(ast)


def parseModule(code, options={}, delegate=None):
    parsingOptions = options or {}
    parsingOptions['sourceType'] = 'module'
    return parse(code, parsingOptions, delegate)


def parseScript(code, options={}, delegate=None):
    parsingOptions = options or {}
    parsingOptions['sourceType'] = 'script'
    return parse(code, parsingOptions, delegate)


def tokenize(code, options={}, delegate=None):
    tokenizer = Tokenizer(code, options)

    class Tokens(list):
        pass

    tokens = Tokens()

    try:
        while True:
            token = tokenizer.getNextToken()
            if not token:
                break
            if delegate:
                token = delegate(token)
            tokens.append(token)
    except Error as e:
        tokenizer.errorHandler.tolerate(e)

    if tokenizer.errorHandler.tolerant:
        tokens.errors = tokenizer.errors()

    return toDict(tokens)
