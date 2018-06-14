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

from __future__ import absolute_import

import os
import re
import json
import glob
import fnmatch
import unittest

from esprima import parse, tokenize, Error, toDict

BASE_DIR = os.path.dirname(__file__)

SOURCE_RE = re.compile(br'''^var\s+source\s*=\s*(['"])(.*)\1;\s*$''', re.DOTALL)

EXPECTED_FAULRES = (
    ('TestExpression', u'u_flag_surrogate_pair'),  # Regex comes with no value
)


def test_factory(_path):
    def test_file(filename):
        result_path = os.path.dirname(filename)
        result_syntax_path = os.path.join(result_path, 'syntax')
        if os.path.isdir(result_syntax_path):
            result_path = result_syntax_path
        result_base = os.path.join(result_path, os.path.basename(os.path.splitext(filename.replace('.source.', '.'))[0]))
        for result_type in ('', '.tree', '.tokens', '.failure'):
            result_file = '%s%s.json' % (result_base, result_type)
            if os.path.exists(result_file):
                if not result_type:
                    result_type = '.tree'
                break
        else:
            return

        def test(self):
            with open(result_file, 'rb') as f:
                expected_json = f.read()
            expected = toDict(json.loads(expected_json.decode('utf-8')))
            if isinstance(expected, dict):
                expected.pop('description', None)  # Not all json failure files include description
                expected.pop('tokenize', None)  # tokenize is not part of errors
                options = expected.pop('options', None)  # Extracts options from tree (if any)
            else:
                options = None

            with open(filename, 'rb') as f:
                actual_code = f.read()
            if '.source.' in filename:
                actual_code = SOURCE_RE.sub(r'\2', actual_code).decode('unicode_escape')
            else:
                actual_code = actual_code.decode('utf-8')

            try:
                if result_type == '.tokens':
                    if options is None:
                        options = {
                            'loc': True,
                            'range': True,
                            'comment': True,
                            'tolerant': True,
                        }
                    actual = toDict(tokenize(actual_code, options=options))
                else:
                    sourceType = 'module' if '.module.' in filename else 'script'
                    if options is None:
                        options = {
                            'jsx': True,
                            'comment': 'comments' in expected,
                            'range': True,
                            'loc': True,
                            'tokens': True,
                            'raw': True,
                            'tolerant': 'errors' in expected,
                            'source': None,
                            'sourceType': expected.get('sourceType', sourceType),
                        }

                    if options.get('comment'):
                        def hasAttachedComment(expected):
                            for k, v in expected.items():
                                if k in ('leadingComments', 'trailingComments', 'innerComments'):
                                    return True
                                elif isinstance(v, dict):
                                    if hasAttachedComment(v):
                                        return True
                                elif isinstance(v, list):
                                    for i in v:
                                        if isinstance(i, dict):
                                            if hasAttachedComment(i):
                                                return True
                            return False
                        options['attachComment'] = hasAttachedComment(expected)

                    if expected.get('tokens'):
                        token = expected['tokens'][0]
                        options['range'] = 'range' in token
                        options['loc'] = 'loc' in token

                    if expected.get('comments'):
                        comment = expected['comments'][0]
                        options['range'] = 'range' in comment
                        options['loc'] = 'loc' in comment

                    if options.get('loc'):
                        options['source'] = expected.get('loc', {}).get('source')

                    actual = toDict(parse(actual_code, options=options))
            except Error as e:
                actual = e.toDict()

            self.assertEqual(expected, actual)

        test_name = os.path.basename(os.path.splitext(filename)[0])
        test_name = re.sub(r'[-. _]+', '_', test_name)
        if not test_name.isupper():
            test_name = re.sub(r'(?<=[^_])([A-Z])', r'_\1', test_name)
        test_name = test_name.lower()

        return test_name, test

    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for filename in files:
                if fnmatch.fnmatch(filename, '*.js'):
                    filename = os.path.join(root, filename)
                    test = test_file(filename)
                    if test:
                        yield test
    else:
        test = test_file(path)
        if test:
            yield test


class TestEsprima(unittest.TestCase):
    def test_basic(self):
        expected = {
            "sourceType": "script",
            "type": "Program",
            "body": [
                {
                    "type": "VariableDeclaration",
                    "declarations": [
                        {
                            "type": "VariableDeclarator",
                            "id": {
                                "type": "Identifier",
                                "name": "$"
                            },
                            "init": {
                                "type": "Literal",
                                "value": "Hello!",
                                "raw": '"Hello!"'
                            }
                        }
                    ],
                    "kind": "var"
                }
            ]
        }

        actual = toDict(parse('var $ = "Hello!"'))

        self.assertEqual(expected, actual)


# class TestThirdParty(unittest.TestCase):
#     pass


# for path in glob.glob(os.path.join(BASE_DIR, '3rdparty', '*.js')):
#     for test_name, test in test_factory(path):
#         setattr(TestThirdParty, 'test_%s' % test_name, test)


for fixture_path in glob.glob(os.path.join(BASE_DIR, 'fixtures', '*')):
    class_name = os.path.basename(fixture_path).replace('-', ' ').replace('.', ' ')
    class_name = 'Test%s' % ''.join((n.capitalize() if n.islower() else n) for n in class_name.split())
    Test = type(class_name, (unittest.TestCase,), {'maxDiff': None})  # {'maxDiff': None}
    globals()[class_name] = Test
    for path in glob.glob(os.path.join(fixture_path, '*')):
        if os.path.isdir(path) or fnmatch.fnmatch(path, '*.js'):
            for test_name, test in test_factory(path):
                if (class_name, test_name) in EXPECTED_FAULRES:
                    test = unittest.expectedFailure(test)
                setattr(Test, 'test_%s' % test_name, test)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
