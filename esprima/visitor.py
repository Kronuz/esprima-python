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

from .nodes import Node


class NodeVisitor(object):
    """
    A node visitor base class that walks the abstract syntax tree and calls a
    visitor function for every node found.  This function may return a value
    which is forwarded by the `visit` method.

    This class is meant to be subclassed, with the subclass adding visitor
    methods.

    Per default the visitor functions for the nodes are ``'visit_'`` +
    class name of the node.  So a `Module` node visit function would
    be `visit_Module`.  This behavior can be changed by overriding
    the `visit` method.  If no visitor function exists for a node
    (return value `None`) the `generic_visit` visitor is used instead.
    """

    def __call__(self, node, metadata):
        return self.transform(node, metadata)

    def transform(self, node, metadata):
        """Transform a node."""
        if isinstance(node, Node):
            method = 'transform_' + node.__class__.__name__
            transformer = getattr(self, method, self.generic_transform)
            new_node = transformer(node, metadata)
            if new_node is not None and node is not new_node:
                node = new_node
        return node

    def generic_transform(self, node, metadata):
        """Called if no explicit transform function exists for a node."""
        return node

    def visit(self, node):
        """Visit a node."""
        if isinstance(node, Node):
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            new_node = visitor(node)
            if new_node is not None and node is not new_node:
                node = new_node
        return node

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node."""
        for field, value in list(node.__dict__.items()):
            if not field.startswith('_'):
                if isinstance(value, list):
                    for i, item in enumerate(value):
                        new_item = self.visit(item)
                        if new_item is not None and item is not new_item:
                            value[i] = new_item
                else:
                    new_value = self.visit(value)
                    if new_value is not None and value is not new_value:
                        node.__dict__[field] = new_value
        return node
