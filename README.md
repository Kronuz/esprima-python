[![PyPI version](https://img.shields.io/pypi/v/esprima.svg)](https://pypi.python.org/pypi/esprima)
[![PyPI downloads](https://img.shields.io/pypi/dm/esprima.svg)](https://pypi.python.org/pypi/esprima)

**Esprima** ([esprima.org](http://esprima.org), BSD license) is a high performance,
standard-compliant [ECMAScript](http://www.ecma-international.org/publications/standards/Ecma-262.htm)
parser officially written in ECMAScript (also popularly known as
[JavaScript](https://en.wikipedia.org/wiki/JavaScript)) and ported to Python.
Esprima is created and maintained by [Ariya Hidayat](https://twitter.com/ariyahidayat),
with the help of [many contributors](https://github.com/jquery/esprima/contributors).

Python port is a line-by-line manual translation and was created and is maintained by [German Mendez Bravo (Kronuz)](https://twitter.com/germbravo).

### Features

- Full support for ECMAScript 2017 ([ECMA-262 8th Edition](http://www.ecma-international.org/publications/standards/Ecma-262.htm))
- Sensible [syntax tree format](https://github.com/estree/estree/blob/master/es5.md) as standardized by [ESTree project](https://github.com/estree/estree)
- Experimental support for [JSX](https://facebook.github.io/jsx/), a syntax extension for [React](https://facebook.github.io/react/)
- Optional tracking of syntax node location (index-based and line-column)
- [Heavily tested](http://esprima.org/test/ci.html) (~1500 [unit tests](https://github.com/jquery/esprima/tree/master/test/fixtures) with [full code coverage](https://codecov.io/github/jquery/esprima))

### Installation

```shell
pip install esprima
```

### API

Esprima can be used to perform [lexical analysis](https://en.wikipedia.org/wiki/Lexical_analysis) (tokenization) or [syntactic analysis](https://en.wikipedia.org/wiki/Parsing) (parsing) of a JavaScript program.

A simple example:

```python
>>> import esprima
>>> program = 'const answer = 42'

>>> esprima.tokenize(program)
[{ type: "Keyword", value: "const" },
 { type: "Identifier", value: "answer" },
 { type: "Punctuator", value: "=" },
 { type: "Numeric", value: "42" }]

>>> esprima.parseScript(program)
{ body: [{ kind: "const", declarations: [{ init: { raw: "42", type: "Literal", value: 42 }, type: "VariableDeclarator", id: { type: "Identifier", name: "answer" } }], type: "VariableDeclaration" }], type: "Program", sourceType: "script" }
```

For more information, please read the [complete documentation](http://esprima.org/doc).
