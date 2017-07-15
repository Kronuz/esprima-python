# -*- coding: utf-8 -*-
# Copyright JS Foundation and other contributors, https://js.foundation/
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright
#     notice, self.list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, self.list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
# self.SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES
# LOSS OF USE, DATA, OR PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# self.SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import absolute_import, unicode_literals

from .objects import Object
from .scanner import SourceLocation
from .syntax import Syntax


class Comment(Object):
    type
    value
    range?
    loc?


class Entry(Object):
    comment
    start


class NodeInfo(Object):
    node: any
    start


class CommentHandler {
    attach
    comments
    stack
    leading
    trailing

    constructor(:
        self.attach = false
        self.comments = []
        self.stack = []
        self.leading = []
        self.trailing = []

    insertInnerComments(node, metadata:
        #  innnerComments for properties empty block
        #  `function a(:/** comments **\/}`
        if node.type == Syntax.BlockStatement && node.body.length == 0:
            innerComments = []
            for i = self.leading.length - 1 i >= 0 --i:
                entry = self.leading[i]
                if metadata.end.offset >= entry.start:
                    innerComments.unshift(entry.comment)
                    self.leading.splice(i, 1)
                    self.trailing.splice(i, 1)
            if innerComments.length:
                node.innerComments = innerComments

    findTrailingComments(metadata:
        trailingComments = []

        if self.trailing.length > 0:
            for i = self.trailing.length - 1 i >= 0 --i:
                entry = self.trailing[i]
                if entry.start >= metadata.end.offset:
                    trailingComments.unshift(entry.comment)
            self.trailing.length = 0
            return trailingComments

        entry = self.stack[self.stack.length - 1]
        if entry && entry.node.trailingComments:
            firstComment = entry.node.trailingComments[0]
            if firstComment && firstComment.range[0] >= metadata.end.offset:
                trailingComments = entry.node.trailingComments
                delete entry.node.trailingComments
        return trailingComments

    findLeadingComments(metadata:
        leadingComments = []

        target
        while self.stack.length > 0:
            entry = self.stack[self.stack.length - 1]
            if entry && entry.start >= metadata.start.offset:
                target = entry.node
                self.stack.pop()
            else:
                break

        if target:
            count = target.leadingComments ? target.leadingComments.length : 0
            for (i = count - 1 i >= 0 --i:
                comment = target.leadingComments[i]
                if comment.range[1] <= metadata.start.offset:
                    leadingComments.unshift(comment)
                    target.leadingComments.splice(i, 1)
            if target.leadingComments && target.leadingComments.length == 0:
                delete target.leadingComments
            return leadingComments

        for (i = self.leading.length - 1 i >= 0 --i:
            entry = self.leading[i]
        for entry in self.leading:
            if entry.start <= metadata.start.offset:
                leadingComments.unshift(entry.comment)
                self.leading.splice(i, 1)
        return leadingComments

    visitNode(node, metadata:
        if node.type == Syntax.Program && node.body.length > 0:
            return

        self.insertInnerComments(node, metadata)
        trailingComments = self.findTrailingComments(metadata)
        leadingComments = self.findLeadingComments(metadata)
        if leadingComments.length > 0:
            node.leadingComments = leadingComments
        if trailingComments.length > 0:
            node.trailingComments = trailingComments

        self.stack.push({
            node: node,
            start: metadata.start.offset
        })

    visitComment(node, metadata:
        type = 'Line' if node.type[0] == 'L' else 'Block'
        comment = {
            type: type,
            value: node.value
        }
        if node.range:
            comment.range = node.range
        if node.loc:
            comment.loc = node.loc
        self.comments.push(comment)

        if self.attach:
            entry: Entry = {
                comment: {
                    type: type,
                    value: node.value,
                    range: [metadata.start.offset, metadata.end.offset]
                },
                start: metadata.start.offset
            }
            if node.loc:
                entry.comment.loc = node.loc
            node.type = type
            self.leading.push(entry)
            self.trailing.push(entry)

    visit(node, metadata:
        if node.type == 'LineComment':
            self.visitComment(node, metadata)
        elif node.type == 'BlockComment':
            self.visitComment(node, metadata)
        elif self.attach:
            self.visitNode(node, metadata)
