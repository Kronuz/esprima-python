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

from .nodes import Expression
from .jsx_syntax import JSXSyntax


class JSXClosingElement(Expression):
    def __init__(self, name):
        super(JSXClosingElement, self).__init__(
            type=JSXSyntax.JSXClosingElement,
            name=name,
        )


class JSXElement(Expression):
    def __init__(self, openingElement, children, closingElement):
        super(JSXElement, self).__init__(
            type=JSXSyntax.JSXElement,
            openingElement=openingElement,
            children=children,
            closingElement=closingElement,
        )


class JSXEmptyExpression(Expression):
    def __init__(self):
        super(JSXEmptyExpression, self).__init__(
            type=JSXSyntax.JSXEmptyExpression,
        )


class JSXExpressionContainer(Expression):
    def __init__(self, expression):
        super(JSXExpressionContainer, self).__init__(
            type=JSXSyntax.JSXExpressionContainer,
            expression=expression,
        )


class JSXIdentifier(Expression):
    def __init__(self, name):
        super(JSXIdentifier, self).__init__(
            type=JSXSyntax.JSXIdentifier,
            name=name,
        )


class JSXMemberExpression(Expression):
    def __init__(self, object, property):
        super(JSXMemberExpression, self).__init__(
            type=JSXSyntax.JSXMemberExpression,
            object=object,
            property=property,
        )


class JSXAttribute(Expression):
    def __init__(self, name, value):
        super(JSXAttribute, self).__init__(
            type=JSXSyntax.JSXAttribute,
            name=name,
            value=value,
        )


class JSXNamespacedName(Expression):
    def __init__(self, namespace, name):
        super(JSXNamespacedName, self).__init__(
            type=JSXSyntax.JSXNamespacedName,
            namespace=namespace,
            name=name,
        )


class JSXOpeningElement(Expression):
    def __init__(self, name, selfClosing, attributes):
        super(JSXOpeningElement, self).__init__(
            type=JSXSyntax.JSXOpeningElement,
            name=name,
            selfClosing=selfClosing,
            attributes=attributes,
        )


class JSXSpreadAttribute(Expression):
    def __init__(self, argument):
        super(JSXSpreadAttribute, self).__init__(
            type=JSXSyntax.JSXSpreadAttribute,
            argument=argument,
        )


class JSXText(Expression):
    def __init__(self, value, raw):
        super(JSXText, self).__init__(
            type=JSXSyntax.JSXText,
            value=value,
            raw=raw,
        )
