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

from .objects import Object
from .syntax import Syntax


class Node(Object):
    def __dir__(self):
        return list(self.__dict__.keys())

    def __iter__(self):
        return self.__iter__

    def keys(self):
        return self.__dict__.keys()

    def items(self):
        return self.__dict__.items()


class Expression(Node):
    """Any expression node. Since the left-hand side of an assignment
    may be any expression in general, an expression can also be a pattern."""


class Pattern(Node):
    pass


class Statement(Node):
    """Any statement."""


class Declaration(Statement):
    pass


class ModuleDeclaration(Node):
    """A module `import` or `export` declaration."""


class ModuleSpecifier(Node):
    def __init__(self, local):
        # type: (Identifier) -> None
        """A specifier in an import or export declaration."""
        self.local = local


class Decorator(Node):
    def __init__(self, expression):
        # type: (Expression) -> None
        self.type = Syntax.Decorator
        self.expression = expression


class Function(Node):
    def __init__(self, id, generator, async, params, body):
        # type: (Optional[Identifier], bool, bool, List[Pattern], BlockStatement) -> None
        """A function declaration or expression."""
        self.id = id
        self.generator = generator
        self.async = async
        self.params = params
        self.body = body


class FunctionDeclaration(Function, Declaration):
    def __init__(self, id, params, body, generator):
        # type: (Identifier, List[Pattern], BlockStatement, bool) -> None
        """A function declaration. Note that unlike in the parent interface
        `Function`, the `id` cannot be `null`, except when this is the child of
        an `ExportDefaultDeclaration`."""
        Function.__init__(self, id=id, generator=generator, async=False, params=params, body=body)
        self.type = Syntax.FunctionDeclaration
        self.expression = False


class ArrayExpression(Expression):
    def __init__(self, elements):
        # type: (Optional[Union[Expression, SpreadElement]]) -> None
        """An array expression."""
        self.type = Syntax.ArrayExpression
        self.elements = elements


class ArrayPattern(Pattern):
    def __init__(self, elements):
        # type: (Optional[List[Pattern]]) -> None
        self.type = Syntax.ArrayPattern
        self.elements = elements


class ArrowFunctionExpression(Function, Expression):
    def __init__(self, params, body, expression):
        # type: (List[Pattern], Union[BlockStatement, Expression], bool) -> None
        """A fat arrow function expression, e.g., `let foo = (bar) => { /* body */ }`."""
        Function.__init__(self, id=None, generator=False, async=False, params=params, body=body)
        self.type = Syntax.ArrowFunctionExpression
        self.expression = expression


class AssignmentExpression(Expression):
    AssignmentOperator = set(("=", "+=", "-=", "*=", "/=", "%=", "<<=", ">>=", ">>>=", "|=", "^=", "&="))

    def __init__(self, operator, left, right):
        # type: (str, Union[Pattern, Expression], Expression) -> None
        """An assignment operator expression."""
        self.type = Syntax.AssignmentExpression
        self.operator = operator
        self.left = left
        self.right = right


class AssignmentPattern(Pattern):
    def __init__(self, left, right):
        # type: (Pattern, Expression) -> None
        self.type = Syntax.AssignmentPattern
        self.left = left
        self.right = right


class AsyncArrowFunctionExpression(Function, Expression):
    def __init__(self, params, body, expression):
        # type: (List[Pattern], Union[BlockStatement, Expression], bool) -> None
        """A fat arrow async function expression, e.g., `let foo = async (bar) => { /* body */ }`."""
        Function.__init__(self, id=None, generator=False, async=True, params=params, body=body)
        self.type = Syntax.ArrowFunctionExpression
        self.expression = expression


class AsyncFunctionDeclaration(Function, Declaration):
    def __init__(self, id, params, body):
        # type: (Identifier, List[Pattern], BlockStatement) -> None
        """An async function declaration. Note that unlike in the parent
        interface `Function`, the `id` cannot be `null`, except when this
        is the child of an `ExportDefaultDeclaration`."""
        Function.__init__(self, id=id, generator=False, async=True, params=params, body=body)
        self.type = Syntax.FunctionDeclaration
        self.expression = False


class AsyncFunctionExpression(Function, Expression):
    def __init__(self, id, params, body):
        # type: (Identifier, List[Pattern], BlockStatement) -> None
        """An async function expression."""
        Function.__init__(self, id=id, generator=False, async=True, params=params, body=body)
        self.type = Syntax.FunctionExpression
        self.expression = False


class AwaitExpression(Expression):
    def __init__(self, argument):
        # type: (Optional[Expression]) -> None
        """A `await` expression."""
        self.type = Syntax.AwaitExpression
        self.argument = argument


class BinaryExpression(Expression):
    BinaryOperator = set(("==", "!=", "===", "!==", "<", "<=", ">", ">=", "<<", ">>", ">>>", "+", "-", "*", "/", "%", "|", "^", "&", "in", "instanceof"))

    def __init__(self, operator, left, right):
        # type: (str, Expression, Expression) -> None
        """A binary operator expression."""
        self.type = Syntax.BinaryExpression
        self.operator = operator
        self.left = left
        self.right = right


class LogicalExpression(Expression):
    LogicalOperator = set(("||", "&&"))

    def __init__(self, operator, left, right):
        # type: (str, Expression, Expression) -> None
        """A logical operator expression."""
        self.type = Syntax.LogicalExpression
        self.operator = operator
        self.left = left
        self.right = right


class BlockStatement(Statement):
    def __init__(self, body):
        # type: (List[Statement]) -> None
        """A block statement, i.e., a sequence of statements surrounded by braces."""
        self.type = Syntax.BlockStatement
        self.body = body


class BreakStatement(Statement):
    def __init__(self, label):
        # type: (Optional[Identifier]) -> None
        """A `break` statement."""
        self.type = Syntax.BreakStatement
        self.label = label


class CallExpression(Expression):
    def __init__(self, callee, args, optional=None):
        # type: (Union[Expression, Super, Import], List[Union[Expression, SpreadElement]], Optional[bool]) -> None
        """A function or method call expression."""
        self.type = Syntax.CallExpression
        self.callee = callee
        self.arguments = args
        self.optional = optional


class CatchClause(Node):
    def __init__(self, param, body):
        # type: (Optional[Pattern], BlockStatement) -> None
        """A `catch` clause following a `try` block."""
        self.type = Syntax.CatchClause
        self.param = param
        self.body = body


class Super(Node):
    def __init__(self):
        # type: () -> None
        """A `super` pseudo-expression."""
        self.type = Syntax.Super


class Class(Node):
    # Originally not in esprima
    def __init__(self, id, superClass, body, decorators=None):
        # type: (Optional[Identifier], Optional[Expression], ClassBody, Optional[List[Decorator]]) -> None
        """Abstract base class"""
        self.id = id
        self.superClass = superClass
        self.body = body
        self.decorators = [] if decorators is None else decorators


class ClassBody(Node):
    def __init__(self, body):
        # type: (List[ClassMethod, ClassProperty, ClassPrivateProperty]) -> None
        self.type = Syntax.ClassBody
        self.body = body


class ClassDeclaration(Class, Declaration):
    def __init__(self, id, superClass, body, decorators=None):
        # type: (Identifier, Optional[Expression], ClassBody, Optional[List[Decorator]]) -> None
        Class.__init__(self, id=id, superClass=superClass, body=body, decorators=decorators)
        self.type = Syntax.ClassDeclaration


class ClassExpression(Class, Expression):
    def __init__(self, id, superClass, body, decorators=None):
        # type: (Optional[Identifier], Optional[Expression], ClassBody, Optional[List[Decorator]]) -> None
        Class.__init__(self, id=id, superClass=superClass, body=body, decorators=decorators)
        self.type = Syntax.ClassExpression


class ComputedMemberExpression(Expression, Pattern):
    def __init__(self, object, property, optional=None):
        # type: (Union[Expression, Super], Expression, Optional[bool]) -> None
        """A member expression. The node corresponds to a computed (`a[b]``)
        member expression and `property` is an `Expression`. The optional
        flags indicates that the member expression can be called even
        if the object is null or undefined. If this is the object value
        (null/undefined) should be returned."""
        self.type = Syntax.MemberExpression
        self.computed = True
        self.object = object
        self.property = property
        self.optional = optional


class ConditionalExpression(Expression):
    def __init__(self, test, consequent, alternate):
        # type: (Expression, Expression, Expression) -> None
        """A conditional expression, i.e., a ternary `?`/`:` expression."""
        self.type = Syntax.ConditionalExpression
        self.test = test
        self.consequent = consequent
        self.alternate = alternate


class ContinueStatement(Statement):
    def __init__(self, label):
        # type: (Optional[Identifier]) -> None
        """A `continue` statement."""
        self.type = Syntax.ContinueStatement
        self.label = label


class DebuggerStatement(Statement):
    def __init__(self):
        # type: () -> None
        """A `debugger` statement."""
        self.type = Syntax.DebuggerStatement


class Directive(Node):
    def __init__(self, expression, directive):
        # type: (Expression, DirectiveLiteral) -> None
        self.type = Syntax.ExpressionStatement
        self.expression = expression
        self.directive = directive


class DoWhileStatement(Statement):
    def __init__(self, body, test):
        # type: (Statement, Expression) -> None
        """A `do`/`while` statement."""
        self.type = Syntax.DoWhileStatement
        self.body = body
        self.test = test


class EmptyStatement(Statement):
    def __init__(self):
        # type: () -> None
        """An empty statement, i.e., a solitary semicolon."""
        self.type = Syntax.EmptyStatement


class ExportAllDeclaration(Declaration):
    def __init__(self, source):
        # type: (Literal) -> None
        """An export batch declaration, e.g., `export * from "mod";`."""
        self.type = Syntax.ExportAllDeclaration
        self.source = source


class OptFunctionDeclaration(FunctionDeclaration):
    def __init__(self, id, params, body, generator):
        # type: (Optional[Identifier], List[Pattern], BlockStatement, bool) -> None
        FunctionDeclaration.__init__(self, id=id, params=params, body=body, generator=generator)


class OptAsyncFunctionDeclaration(AsyncFunctionDeclaration):
    def __init__(self, id, params, body):
        # type: (Optional[Identifier], List[Pattern], BlockStatement) -> None
        AsyncFunctionDeclaration.__init__(self, id=id, params=params, body=body)
        self.type = Syntax.FunctionDeclaration
        self.expression = False


class OptClassDeclaration(ClassDeclaration):
    def __init__(self, id, superClass, body, decorators=None):
        # type: (Optional[Identifier], Optional[Expression], ClassBody, Optional[List[Decorator]]) -> None
        ClassDeclaration.__init__(self, id=id, superClass=superClass, body=body, decorators=decorators)


class ExportDefaultDeclaration(ModuleDeclaration):
    def __init__(self, declaration):
        # type: (Union[OptFunctionDeclaration, OptAsyncFunctionDeclaration, OptClassDeclaration, Expression]) -> None
        """An export default declaration, e.g., `export default function () {};`
        or `export default 1;`."""
        self.type = Syntax.ExportDefaultDeclaration
        self.declaration = declaration


class ExportNamedDeclaration(ModuleDeclaration):
    def __init__(self, declaration, specifiers, source):
        # type: (Optional[Declaration], List[ExportSpecifier], Optional[Literal]) -> None
        """An export named declaration, e.g., `export {foo, bar};`,
        `export {foo} from "mod";`, `export var foo = 1;` or
        `export * as foo from "bar";`.

        Note: Having declaration populated with non-empty specifiers
        or non-null source results in an invalid state.
        """
        self.type = Syntax.ExportNamedDeclaration
        self.declaration = declaration
        self.specifiers = specifiers
        self.source = source


class ExportSpecifier(ModuleSpecifier):
    def __init__(self, local, exported):
        # type: (Identifier, Identifier) -> None
        """An exported variable binding, e.g., `{foo}` in `export {foo}`
        or `{bar as foo}` in `export {bar as foo}`. The `exported` field
        refers to the name exported in the module. The `local` field
        refers to the binding into the local module scope. If it is a
        basic named export, such as in `export {foo}`, both `exported`
        and `local` are equivalent `Identifier` nodes; in this case an
        `Identifier` node representing `foo`. If it is an aliased export,
        such as in `export {bar as foo}`, the `exported` field is an
        `Identifier` node representing `foo`, and the `local` field is
        an `Identifier` node representing `bar`."""
        self.type = Syntax.ExportSpecifier
        self.exported = exported
        self.local = local


class ExpressionStatement(Statement):
    def __init__(self, expression):
        # type: (Expression) -> None
        """An expression statement, i.e., a statement consisting of a single expression."""
        self.type = Syntax.ExpressionStatement
        self.expression = expression


class ForInStatement(Statement):
    def __init__(self, left, right, body):
        # type: (Union[VariableDeclaration, Expression], Optional[Expression], Statement) -> None
        """A `for`/`in` statement."""
        self.type = Syntax.ForInStatement
        self.each = False
        self.left = left
        self.right = right
        self.body = body


class ForOfStatement(ForInStatement):
    def __init__(self, left, right, body):
        # type: (Union[VariableDeclaration, Expression], Optional[Expression], Statement) -> None
        ForInStatement.__init__(self, left=left, right=right, body=body)
        self.type = Syntax.ForOfStatement


class ForStatement(Statement):
    def __init__(self, init, test, update, body):
        # type: (Optional[Union[VariableDeclaration, Expression]], Optional[Expression], Optional[Expression], Statement) -> None
        """A `for` statement."""
        self.type = Syntax.ForStatement
        self.init = init
        self.test = test
        self.update = update
        self.body = body


class FunctionExpression(Function, Expression):
    def __init__(self, id, params, body, generator):
        # type: (Identifier, List[Pattern], BlockStatement, bool) -> None
        """A function expression."""
        Function.__init__(self, id=id, generator=generator, async=False, params=params, body=body)
        self.type = Syntax.FunctionExpression
        self.expression = False


class Identifier(Expression, Pattern):
    def __init__(self, name):
        # type: (str) -> None
        """An identifier. Note that an identifier may be an expression or a destructuring pattern."""
        self.type = Syntax.Identifier
        self.name = name


class PrivateName(Expression, Pattern):
    def __init__(self, name):
        # type: (Identifier) -> None
        """A Private Name Identifier."""
        self.type = Syntax.Identifier
        self.name = name


class IfStatement(Statement):
    def __init__(self, test, consequent, alternate):
        # type: (Expression, Statement, Optional[Statement]) -> None
        """An `if` statement."""
        self.type = Syntax.IfStatement
        self.test = test
        self.consequent = consequent
        self.alternate = alternate


class Import(Node):
    def __init__(self):
        # type: () -> None
        """A `import` pseudo-expression."""
        self.type = Syntax.Import


class ImportDeclaration(ModuleDeclaration):
    def __init__(self, specifiers, source):
        # type: (List[Union[ImportSpecifier, ImportDefaultSpecifier, ImportNamespaceSpecifier]], Literal) -> None
        """An import declaration, e.g., `import foo from "mod";`."""
        self.type = Syntax.ImportDeclaration
        self.specifiers = specifiers
        self.source = source


class ImportDefaultSpecifier(ModuleSpecifier):
    def __init__(self, local):
        # type: (Identifier) -> None
        """A default import specifier, e.g., `foo` in `import foo from "mod.js"`."""
        self.type = Syntax.ImportDefaultSpecifier
        self.local = local


class ImportNamespaceSpecifier(ModuleSpecifier):
    def __init__(self, local):
        # type: (Identifier) -> None
        """A namespace import specifier, e.g., `* as foo` in `import * as foo from "mod.js"`."""
        self.type = Syntax.ImportNamespaceSpecifier
        self.local = local


class ImportSpecifier(ModuleSpecifier):
    def __init__(self, local, imported):
        # type: (Identifier, Identifier) -> None
        """An imported variable binding, e.g., `{foo}`` in `import {foo} from "mod"`
        or `{foo as bar}`` in `import {foo as bar} from "mod"`. The `imported`
        field refers to the name of the export imported from the module. The `local`
        field refers to the binding imported into the local module scope. If it
        is a basic named import, such as in `import {foo} from "mod"`, both
        `imported` and `local` are equivalent `Identifier` nodes; in this case an
        `Identifier` node representing `foo`. If it is an aliased import, such as
        in `import {foo as bar} from "mod"`, the `imported` field is an `Identifier`
        node representing `foo`, and the `local` field is an `Identifier` node
        representing `bar`."""
        self.type = Syntax.ImportSpecifier
        self.local = local
        self.imported = imported


class LabeledStatement(Statement):
    def __init__(self, label, body):
        # type: (Identifier, Statement) -> None
        """A labeled statement, i.e., a statement prefixed by a `break`/`continue` label."""
        self.type = Syntax.LabeledStatement
        self.label = label
        self.body = body


class Literal(Expression):
    """A literal token. May or may not represent an expression."""


class RegExpLiteral(Literal):
    # Originally named RegexLiteral in esprima
    def __init__(self, pattern, flags, raw):
        # type: (str, str, str) -> None
        self.type = Syntax.RegExpLiteral
        self.pattern = pattern
        self.flags = flags
        self.raw = raw


class NullLiteral(Literal):
    def __init__(self, raw):
        # type: (str) -> None
        self.type = Syntax.NullLiteral
        self.raw = raw


class StringLiteral(Literal):
    def __init__(self, value, raw):
        # type: (str, str) -> None
        self.type = Syntax.StringLiteral
        self.value = value
        self.raw = raw


class BooleanLiteral(Literal):
    def __init__(self, value, raw):
        # type: (bool, str) -> None
        self.type = Syntax.BooleanLiteral
        self.value = value
        self.raw = raw


class NumericLiteral(Literal):
    def __init__(self, value, raw):
        # type: (Union[float, int], str) -> None
        self.type = Syntax.NumericLiteral
        self.value = value
        self.raw = raw


class DirectiveLiteral(StringLiteral):
    def __init__(self, value, raw):
        # type: (str) -> None
        StringLiteral.__init__(self, value=value, raw=raw)
        self.type = Syntax.ExpressionStatement


class MetaProperty(Node):
    def __init__(self, meta, property):
        # type: (Identifier, Identifier) -> None
        self.type = Syntax.MetaProperty
        self.meta = meta
        self.property = property


class ClassMethod(Function):
    # Originally named MethodDefinition in esprima
    def __init__(self, key, computed, generator, async, params, body, kind, isStatic, decorators=None):
        # type: (Expression, bool, bool, bool, List[Pattern], BlockStatement, str, bool, Optional[List[Decorator]]) -> None
        """A class method declaration."""
        Function.__init__(self, generator=generator, async=async, params=params, body=body)
        self.type = Syntax.ClassMethod
        self.key = key
        self.computed = computed
        self.kind = kind  # "constructor" | "method" | "get" | "set"
        self.static = isStatic
        self.decorators = [] if decorators is None else decorators


class ClassProperty(Node):
    # Originally not in esprima
    def __init__(self, key, computed, value, isStatic):
        # type: (Expression, bool, Expression, bool) -> None
        self.type = Syntax.ClassProperty
        self.key = key
        self.computed = computed
        self.value = value
        self.static = isStatic


class ClassPrivateProperty(Node):
    def __init__(self, key, value, isStatic):
        # type: (Identifier, Expression, bool) -> None
        self.type = Syntax.ClassPrivateProperty
        self.key = key
        self.value = value
        self.static = isStatic


class Module(Node):
    def __init__(self, body):
        # type: (ModuleDeclaration) -> None
        """A complete program source tree parsed as an ES6 module."""
        self.type = Syntax.Program
        self.sourceType = 'module'
        self.body = body


class NewExpression(CallExpression):
    def __init__(self, callee, args, optional=None):
        # type: (Union[Expression, Super, Import], List[Union[Expression, SpreadElement]], Optional[bool]) -> None
        """A `new` expression."""
        CallExpression.__init__(self, callee=callee, args=args, optional=optional)
        self.type = Syntax.NewExpression


class ObjectExpression(Expression):
    def __init__(self, properties):
        # type: (Union[ObjectProperty, ObjectMethod, SpreadElement]) -> None
        """An object expression."""
        self.type = Syntax.ObjectExpression
        self.properties = properties


class ObjectMember(Node):
    def __init__(self, key, computed, decorators=None):
        # type: (Expression, bool, Optional[List[Decorator]]) -> None
        """Original Property is split in ObjectProperty and ObjectMethod"""
        self.key = key
        self.computed = computed
        self.decorators = [] if decorators is None else decorators


class ObjectProperty(ObjectMember):
    def __init__(self, key, computed, value, shorthand):
        # type: (Expression, bool, Expression, bool) -> None
        """An object property."""
        ObjectMember.__init__(self, key=key, computed=computed)
        self.type = Syntax.ObjectProperty
        self.shorthand = shorthand
        self.value = value


class ObjectMethod(ObjectMember, Function):
    def __init__(self, kind, key, computed, generator, async, params, body):
        # type: (str, Expression, bool, bool, bool, List[Pattern], BlockStatement) -> None
        """An object method."""
        ObjectMember.__init__(self, key=key, computed=computed)
        self.type = Syntax.ObjectMethod
        self.kind = kind  # "get" | "set" | "method"


class AssignmentProperty(ObjectProperty):
    def __init__(self, key, computed, value, shorthand):
        # type: (Expression, bool, Pattern, bool) -> None
        """An object property."""
        ObjectProperty.__init__(self, key=key, computed=computed, value=value, shorthand=shorthand)


class ObjectPattern(Pattern):
    def __init__(self, properties):
        # type: (List[Union[AssignmentProperty, RestElement]]) -> None
        self.type = Syntax.ObjectPattern
        self.properties = properties


class RestElement(Node):
    def __init__(self, argument):
        # type: (Pattern) -> None
        self.type = Syntax.RestElement
        self.argument = argument


class ReturnStatement(Statement):
    def __init__(self, argument):
        # type: (Optional[Expression]) -> None
        """A `return` statement."""
        self.type = Syntax.ReturnStatement
        self.argument = argument


class Script(Node):
    def __init__(self, body):
        # type: (Statement) -> None
        """A complete program source tree parsed as scripy."""
        self.type = Syntax.Program
        self.sourceType = 'script'
        self.body = body


class SequenceExpression(Expression):
    def __init__(self, expressions):
        # type: (List[Expression]) -> None
        """A sequence expression, i.e., a comma-separated sequence of expressions."""
        self.type = Syntax.SequenceExpression
        self.expressions = expressions


class DoExpression(Expression):
    # Originally not in esprima
    def __init__(self, body):
        # type(BlockStatement) -> None
        self.type = Syntax.DoExpression
        self.body = body


class SpreadElement(Node):
    def __init__(self, argument):
        # type: (Expression) -> None
        """A spread element."""
        self.type = Syntax.SpreadElement
        self.argument = argument


class StaticMemberExpression(Expression, Pattern):
    def __init__(self, object, property, optional=None):
        # type: (Union[Expression, Super], Identifier, Optional[bool]) -> None
        """A member expression. The node corresponds to a static (`a.b`)
        member expression and `property` is an `Identifier`. The optional
        flags indicates that the member expression can be called even
        if the object is null or undefined. If this is the object value
        (null/undefined) should be returned."""
        self.type = Syntax.MemberExpression
        self.computed = False
        self.object = object
        self.property = property
        self.optional = optional


class BindExpression(Expression):
    # Originally not in esprima
    def __init__(self, object, callee):
        # type: (Optional[Expression], Expression) -> None
        """A bind expression. If object is null, then callee should be a MemberExpression."""
        self.type = Syntax.BindExpression
        self.object = object
        self.callee = callee


class SwitchCase(Node):
    def __init__(self, test, consequent):
        # type: (Optional[Expression], List[Statement]) -> None
        """A `case` (if `test` is an `Expression`) or `default`
        (if `test === null`) clause in the body of a `switch` statement."""
        self.type = Syntax.SwitchCase
        self.test = test
        self.consequent = consequent


class SwitchStatement(Statement):
    def __init__(self, discriminant, cases):
        # type: (Expression, List[SwitchCase]) -> None
        """A `switch` statement."""
        self.type = Syntax.SwitchStatement
        self.discriminant = discriminant
        self.cases = cases


class TaggedTemplateExpression(Expression):
    def __init__(self, tag, quasi):
        # type: (Expression, TemplateLiteral) -> None
        self.type = Syntax.TaggedTemplateExpression
        self.tag = tag
        self.quasi = quasi


class TemplateElement(Node):
    class Value(Object):
        def __init__(self, raw, cooked):
            self.raw = raw
            self.cooked = cooked

    def __init__(self, raw, cooked, tail):
        # type: (str, Optional[str], bool) -> None
        self.type = Syntax.TemplateElement
        self.value = TemplateElement.Value(raw, cooked)
        self.tail = tail


class TemplateLiteral(Expression):
    def __init__(self, quasis, expressions):
        # type: (List[TemplateElement], List[Expression]) -> None
        self.type = Syntax.TemplateLiteral
        self.quasis = quasis
        self.expressions = expressions


class ThisExpression(Expression):
    def __init__(self):
        # type: () -> None
        """A `this` expression."""
        self.type = Syntax.ThisExpression


class ThrowStatement(Statement):
    def __init__(self, argument):
        # type: (Expression) -> None
        """A `throw` statement."""
        self.type = Syntax.ThrowStatement
        self.argument = argument


class TryStatement(Statement):
    def __init__(self, block, handler, finalizer):
        # type: (BlockStatement, Optional[CatchClause], Optional[BlockStatement]) -> None
        """A `try` statement. If `handler` is `null` then `finalizer` must be a `BlockStatement`."""
        self.type = Syntax.TryStatement
        self.block = block
        self.handler = handler
        self.finalizer = finalizer


class UnaryExpression(Expression):
    UnaryOperator = set(("-", "+", "!", "~", "typeof", "void", "delete"))

    def __init__(self, operator, argument):
        # type: (str, Expression) -> None
        """A unary operator expression."""
        self.type = Syntax.UnaryExpression
        self.prefix = True
        self.operator = operator  # "-" | "+" | "!" | "~" | "typeof" | "void" | "delete"
        self.argument = argument


class UpdateExpression(Expression):
    UpdateOperator = set(("++", "--"))

    def __init__(self, operator, argument, prefix):
        # type: (str, Expression, bool) -> None
        """An update (increment or decrement) operator expression."""
        self.type = Syntax.UpdateExpression
        self.operator = operator
        self.argument = argument
        self.prefix = prefix


class VariableDeclaration(Declaration):
    def __init__(self, declarations, kind):
        # type: (List[VariableDeclarator], str) -> None
        """A variable declaration."""
        self.type = Syntax.VariableDeclaration
        self.declarations = declarations
        self.kind = kind  # "var" | "let" | "const"


class VariableDeclarator(Node):
    def __init__(self, id, init):
        # type: (Pattern, Optional[Expression]) -> None
        """A variable declarator."""
        self.type = Syntax.VariableDeclarator
        self.id = id
        self.init = init


class WhileStatement(Statement):
    def __init__(self, test, body):
        # type: (Expression, Statement) -> None
        """A `while` statement."""
        self.type = Syntax.WhileStatement
        self.test = test
        self.body = body


class WithStatement(Statement):
    def __init__(self, object, body):
        # type: (Expression, Statement) -> None
        """A `with` statement."""
        self.type = Syntax.WithStatement
        self.object = object
        self.body = body


class YieldExpression(Expression):
    def __init__(self, argument, delegate):
        # type: (Optional[Expression], bool) -> None
        """A `yield` expression."""
        self.type = Syntax.YieldExpression
        self.argument = argument
        self.delegate = delegate


class ArrowParameterPlaceHolder(Node):
    def __init__(self, params):
        self.type = Syntax.ArrowParameterPlaceHolder
        self.params = params
        self.async = False


class AsyncArrowParameterPlaceHolder(Node):
    def __init__(self, params):
        self.type = Syntax.ArrowParameterPlaceHolder
        self.params = params
        self.async = True


class BlockComment(Node):
    def __init__(self, value):
        self.type = Syntax.BlockComment
        self.value = value


class LineComment(Node):
    def __init__(self, value):
        self.type = Syntax.LineComment
        self.value = value
