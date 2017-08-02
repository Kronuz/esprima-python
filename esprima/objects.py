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

import re
import json
from collections import deque

from .compat import unicode


re_type = type(re.compile(r''))


def toDict(value):
    queue = deque()

    def setup(value):
        if isinstance(value, list):
            obj = []
            gen = ((None, v) for v in value)
        elif isinstance(value, dict):
            obj = {}
            gen = ((k, value[k]) for k in value)
        elif isinstance(value, Object):
            obj = {}
            value = value.__dict__
            gen = ((k, value[k]) for k in value)
        elif isinstance(value, re_type):
            obj = {}
            gen = None
        else:
            obj = value
            gen = None
        queue.append((obj, gen))
        return obj

    setup(value)

    while queue:
        obj, gen = queue[-1]

        if gen is None:
            queue.pop()
        else:
            try:
                k, value = next(gen)
            except StopIteration:
                queue.pop()
            else:
                if k is None:
                    obj.append(setup(value))
                elif value is not None:
                    obj[unicode(k)] = setup(value)

    return obj


class Object(object):
    def toDict(self):
        return toDict(self.__dict__)

    def repr(self, obj, level=0, indent=4, nl="\n", sp="", skip=(), reprs=()):
        if isinstance(indent, int):
            indent = " " * indent
        indent1 = indent * level
        indent2 = indent1 + indent
        if isinstance(obj, Object):
            obj = obj.__dict__
        if isinstance(obj, unicode):
            return json.dumps(obj)
        if isinstance(obj, list):
            if not obj:
                return "[]"
            return "[%s%s%s%s%s%s%s]" % (
                sp,
                nl,
                indent2,
                (",%s%s%s" % (nl, sp, indent2)).join(
                    reprs.get(type(v).__name__, self.repr)(v, level=level + 1, indent=indent, nl=nl, sp=sp, skip=skip, reprs=reprs)
                    for v in obj
                ),
                nl,
                indent1,
                sp,
            )
        if isinstance(obj, dict):
            if not obj:
                return "{}"
            return "{%s%s%s%s%s%s%s}" % (
                sp,
                nl,
                indent2,
                (",%s%s%s" % (nl, sp, indent2)).join(
                    reprs.get(type(v).__name__, self.repr)((k, v), level=level + 1, indent=indent, nl=nl, sp=sp, skip=skip, reprs=reprs)
                    for k, v in obj.items()
                    if v is not None and not k.startswith('_') and k not in skip
                ),
                nl,
                indent1,
                sp,
            )
        if isinstance(obj, tuple):
            k, v = obj
            return (
                "%s: %s" % (
                    k, self.repr(v, level=level, indent=indent, nl=nl, sp=sp, skip=skip, reprs=reprs),
                )
            )
        return repr(obj)

    def __repr__(self):
        return self.repr(self, reprs={
            'SourceLocation': lambda o, **k: self.repr(o, **dict(k, indent="", nl="", sp=" ")),
        })

    def __getattr__(self, name):
        return None
