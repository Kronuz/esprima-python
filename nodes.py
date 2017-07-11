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


class Expression(Object):
    pass


class ArrayExpression(Expression):
    def __init__(self, elements):
        super(ArrayExpression, self).__init__(
            type=Syntax.ArrayExpression,
            elements=elements,
        )


class ArrayPattern(Expression):
    def __init__(self, elements):
        super(ArrayPattern, self).__init__(
            type=Syntax.ArrayPattern,
            elements=elements,
        )


class ArrowFunctionExpression(Expression):
    def __init__(self, params, body, expression):
        super(ArrowFunctionExpression, self).__init__(
            type=Syntax.ArrowFunctionExpression,
            generator=False,
            async=False,
            params=params,
            body=body,
            expression=expression,
        )


class AssignmentExpression(Expression):
    def __init__(self, operator, left, right):
        super(AssignmentExpression, self).__init__(
            type=Syntax.AssignmentExpression,
            operator=operator,
            left=left,
            right=right,
        )


class AssignmentPattern(Expression):
    def __init__(self, left, right):
        super(AssignmentPattern, self).__init__(
            type=Syntax.AssignmentPattern,
            left=left,
            right=right,
        )


class AsyncArrowFunctionExpression(Expression):
    def __init__(self, params, body, expression):
        super(AsyncArrowFunctionExpression, self).__init__(
            type=Syntax.ArrowFunctionExpression,
            generator=False,
            async=True,
            params=params,
            body=body,
            expression=expression,
        )


class AsyncFunctionDeclaration(Expression):
    def __init__(self, id, params, body):
        super(AsyncFunctionDeclaration, self).__init__(
            type=Syntax.FunctionDeclaration,
            generator=False,
            expression=False,
            async=True,
            id=id,
            params=params,
            body=body,
        )


class AsyncFunctionExpression(Expression):
    def __init__(self, id, params, body):
        super(AsyncFunctionExpression, self).__init__(
            type=Syntax.FunctionExpression,
            generator=False,
            expression=False,
            async=True,
            id=id,
            params=params,
            body=body,
        )


class AwaitExpression(Expression):
    def __init__(self, argument):
        super(AwaitExpression, self).__init__(
            type=Syntax.AwaitExpression,
            argument=argument,
        )


class BinaryExpression(Expression):
    def __init__(self, operator, left, right):
        super(BinaryExpression, self).__init__(
            type=Syntax.LogicalExpression if operator in ('||', '&&') else Syntax.BinaryExpression,
            operator=operator,
            left=left,
            right=right,
        )


class BlockStatement(Expression):
    def __init__(self, body):
        super(BlockStatement, self).__init__(
            type=Syntax.BlockStatement,
            body=body,
        )


class BreakStatement(Expression):
    def __init__(self, label):
        super(BreakStatement, self).__init__(
            type=Syntax.BreakStatement,
            label=label,
        )


class CallExpression(Expression):
    def __init__(self, callee, args):
        super(CallExpression, self).__init__(
            type=Syntax.CallExpression,
            callee=callee,
            arguments=args,
        )


class CatchClause(Expression):
    def __init__(self, param, body):
        super(CatchClause, self).__init__(
            type=Syntax.CatchClause,
            param=param,
            body=body,
        )


class ClassBody(Expression):
    def __init__(self, body):
        super(ClassBody, self).__init__(
            type=Syntax.ClassBody,
            body=body,
        )


class ClassDeclaration(Expression):
    def __init__(self, id, superClass, body):
        super(ClassDeclaration, self).__init__(
            type=Syntax.ClassDeclaration,
            id=id,
            superClass=superClass,
            body=body,
        )


class ClassExpression(Expression):
    def __init__(self, id, superClass, body):
        super(ClassExpression, self).__init__(
            type=Syntax.ClassExpression,
            id=id,
            superClass=superClass,
            body=body,
        )


class ComputedMemberExpression(Expression):
    def __init__(self, object, property):
        super(ComputedMemberExpression, self).__init__(
            type=Syntax.MemberExpression,
            computed=True,
            object=object,
            property=property,
        )


class ConditionalExpression(Expression):
    def __init__(self, test, consequent, alternate):
        super(ConditionalExpression, self).__init__(
            type=Syntax.ConditionalExpression,
            test=test,
            consequent=consequent,
            alternate=alternate,
        )


class ContinueStatement(Expression):
    def __init__(self, label):
        super(ContinueStatement, self).__init__(
            type=Syntax.ContinueStatement,
            label=label,
        )


class DebuggerStatement(Expression):
    def __init__(self):
        super(DebuggerStatement, self).__init__(
            type=Syntax.DebuggerStatement,
        )


class Directive(Expression):
    def __init__(self, expression, directive):
        super(Directive, self).__init__(
            type=Syntax.ExpressionStatement,
            expression=expression,
            directive=directive,
        )


class DoWhileStatement(Expression):
    def __init__(self, body, test):
        super(DoWhileStatement, self).__init__(
            type=Syntax.DoWhileStatement,
            body=body,
            test=test,
        )


class EmptyStatement(Expression):
    def __init__(self):
        super(EmptyStatement, self).__init__(
            type=Syntax.EmptyStatement,
        )


class ExportAllDeclaration(Expression):
    def __init__(self, source):
        super(ExportAllDeclaration, self).__init__(
            type=Syntax.ExportAllDeclaration,
            source=source,
        )


class ExportDefaultDeclaration(Expression):
    def __init__(self, declaration):
        super(ExportDefaultDeclaration, self).__init__(
            type=Syntax.ExportDefaultDeclaration,
            declaration=declaration,
        )


class ExportNamedDeclaration(Expression):
    def __init__(self, declaration, specifiers, source):
        super(ExportNamedDeclaration, self).__init__(
            type=Syntax.ExportNamedDeclaration,
            declaration=declaration,
            specifiers=specifiers,
            source=source,
        )


class ExportSpecifier(Expression):
    def __init__(self, local, exported):
        super(ExportSpecifier, self).__init__(
            type=Syntax.ExportSpecifier,
            exported=exported,
            local=local,
        )


class ExpressionStatement(Expression):
    def __init__(self, expression):
        super(ExpressionStatement, self).__init__(
            type=Syntax.ExpressionStatement,
            expression=expression,
        )


class ForInStatement(Expression):
    def __init__(self, left, right, body):
        super(ForInStatement, self).__init__(
            type=Syntax.ForInStatement,
            each=False,
            left=left,
            right=right,
            body=body,
        )


class ForOfStatement(Expression):
    def __init__(self, left, right, body):
        super(ForOfStatement, self).__init__(
            type=Syntax.ForOfStatement,
            left=left,
            right=right,
            body=body,
        )


class ForStatement(Expression):
    def __init__(self, init, test, update, body):
        super(ForStatement, self).__init__(
            type=Syntax.ForStatement,
            init=init,
            test=test,
            update=update,
            body=body,
        )


class FunctionDeclaration(Expression):
    def __init__(self, id, params, body, generator):
        super(FunctionDeclaration, self).__init__(
            type=Syntax.FunctionDeclaration,
            expression=False,
            async=False,
            id=id,
            params=params,
            body=body,
            generator=generator,
        )


class FunctionExpression(Expression):
    def __init__(self, id, params, body, generator):
        super(FunctionExpression, self).__init__(
            type=Syntax.FunctionExpression,
            expression=False,
            async=False,
            id=id,
            params=params,
            body=body,
            generator=generator,
        )


class Identifier(Expression):
    def __init__(self, name):
        super(Identifier, self).__init__(
            type=Syntax.Identifier,
            name=name,
        )


class IfStatement(Expression):
    def __init__(self, test, consequent, alternate):
        super(IfStatement, self).__init__(
            type=Syntax.IfStatement,
            test=test,
            consequent=consequent,
            alternate=alternate,
        )


class Import(Expression):
    def __init__(self):
        super(Import, self).__init__(
            type=Syntax.Import,
        )


class ImportDeclaration(Expression):
    def __init__(self, specifiers, source):
        super(ImportDeclaration, self).__init__(
            type=Syntax.ImportDeclaration,
            specifiers=specifiers,
            source=source,
        )


class ImportDefaultSpecifier(Expression):
    def __init__(self, local):
        super(ImportDefaultSpecifier, self).__init__(
            type=Syntax.ImportDefaultSpecifier,
            local=local,
        )


class ImportNamespaceSpecifier(Expression):
    def __init__(self, local):
        super(ImportNamespaceSpecifier, self).__init__(
            type=Syntax.ImportNamespaceSpecifier,
            local=local,
        )


class ImportSpecifier(Expression):
    def __init__(self, local, imported):
        super(ImportSpecifier, self).__init__(
            type=Syntax.ImportSpecifier,
            local=local,
            imported=imported,
        )


class LabeledStatement(Expression):
    def __init__(self, label, body):
        super(LabeledStatement, self).__init__(
            type=Syntax.LabeledStatement,
            label=label,
            body=body,
        )


class Literal(Expression):
    def __init__(self, value, raw):
        super(Literal, self).__init__(
            type=Syntax.Literal,
            value=value,
            raw=raw,
        )


class MetaProperty(Expression):
    def __init__(self, meta, property):
        super(MetaProperty, self).__init__(
            type=Syntax.MetaProperty,
            meta=meta,
            property=property,
        )


class MethodDefinition(Expression):
    def __init__(self, key, computed, value, kind, isStatic):
        super(MethodDefinition, self).__init__(
            type=Syntax.MethodDefinition,
            key=key,
            computed=computed,
            value=value,
            kind=kind,
            static=isStatic,
        )


class Module(Expression):
    def __init__(self, body):
        super(Module, self).__init__(
            type=Syntax.Program,
            sourceType='module',
            body=body,
        )


class NewExpression(Expression):
    def __init__(self, callee, args):
        super(NewExpression, self).__init__(
            type=Syntax.NewExpression,
            callee=callee,
            arguments=args,
        )


class ObjectExpression(Expression):
    def __init__(self, properties):
        super(ObjectExpression, self).__init__(
            type=Syntax.ObjectExpression,
            properties=properties,
        )


class ObjectPattern(Expression):
    def __init__(self, properties):
        super(ObjectPattern, self).__init__(
            type=Syntax.ObjectPattern,
            properties=properties,
        )


class Property(Expression):
    def __init__(self, kind, key, computed, value, method, shorthand):
        super(Property, self).__init__(
            type=Syntax.Property,
            key=key,
            computed=computed,
            value=value,
            kind=kind,
            method=method,
            shorthand=shorthand,
        )


class RegexLiteral(Expression):
    def __init__(self, value, raw, pattern, flags):
        super(RegexLiteral, self).__init__(
            type=Syntax.Literal,
            value=value,
            raw=raw,
            regex={
                'pattern': pattern,
                'flags': flags,
            },
        )


class RestElement(Expression):
    def __init__(self, argument):
        super(RestElement, self).__init__(
            type=Syntax.RestElement,
            argument=argument,
        )


class ReturnStatement(Expression):
    def __init__(self, argument):
        super(ReturnStatement, self).__init__(
            type=Syntax.ReturnStatement,
            argument=argument,
        )


class Script(Expression):
    def __init__(self, body):
        super(Script, self).__init__(
            type=Syntax.Program,
            sourceType='script',
            body=body,
        )


class SequenceExpression(Expression):
    def __init__(self, expressions):
        super(SequenceExpression, self).__init__(
            type=Syntax.SequenceExpression,
            expressions=expressions,
        )


class SpreadElement(Expression):
    def __init__(self, argument):
        super(SpreadElement, self).__init__(
            type=Syntax.SpreadElement,
            argument=argument,
        )


class StaticMemberExpression(Expression):
    def __init__(self, object, property):
        super(StaticMemberExpression, self).__init__(
            type=Syntax.MemberExpression,
            computed=False,
            object=object,
            property=property,
        )


class Super(Expression):
    def __init__(self):
        super(Super, self).__init__(
            type=Syntax.Super,
        )


class SwitchCase(Expression):
    def __init__(self, test, consequent):
        super(SwitchCase, self).__init__(
            type=Syntax.SwitchCase,
            test=test,
            consequent=consequent,
        )


class SwitchStatement(Expression):
    def __init__(self, discriminant, cases):
        super(SwitchStatement, self).__init__(
            type=Syntax.SwitchStatement,
            discriminant=discriminant,
            cases=cases,
        )


class TaggedTemplateExpression(Expression):
    def __init__(self, tag, quasi):
        super(TaggedTemplateExpression, self).__init__(
            type=Syntax.TaggedTemplateExpression,
            tag=tag,
            quasi=quasi,
        )


class TemplateElement(Expression):
    def __init__(self, value, tail):
        super(TemplateElement, self).__init__(
            type=Syntax.TemplateElement,
            value=value,
            tail=tail,
        )


class TemplateLiteral(Expression):
    def __init__(self, quasis, expressions):
        super(TemplateLiteral, self).__init__(
            type=Syntax.TemplateLiteral,
            quasis=quasis,
            expressions=expressions,
        )


class ThisExpression(Expression):
    def __init__(self):
        super(ThisExpression, self).__init__(
            type=Syntax.ThisExpression,
        )


class ThrowStatement(Expression):
    def __init__(self, argument):
        super(ThrowStatement, self).__init__(
            type=Syntax.ThrowStatement,
            argument=argument,
        )


class TryStatement(Expression):
    def __init__(self, block, handler, finalizer):
        super(TryStatement, self).__init__(
            type=Syntax.TryStatement,
            block=block,
            handler=handler,
            finalizer=finalizer,
        )


class UnaryExpression(Expression):
    def __init__(self, operator, argument):
        super(UnaryExpression, self).__init__(
            type=Syntax.UnaryExpression,
            prefix=True,
            operator=operator,
            argument=argument,
        )


class UpdateExpression(Expression):
    def __init__(self, operator, argument, prefix):
        super(UpdateExpression, self).__init__(
            type=Syntax.UpdateExpression,
            operator=operator,
            argument=argument,
            prefix=prefix,
        )


class VariableDeclaration(Expression):
    def __init__(self, declarations, kind):
        super(VariableDeclaration, self).__init__(
            type=Syntax.VariableDeclaration,
            declarations=declarations,
            kind=kind,
        )


class VariableDeclarator(Expression):
    def __init__(self, id, init):
        super(VariableDeclarator, self).__init__(
            type=Syntax.VariableDeclarator,
            id=id,
            init=init,
        )


class WhileStatement(Expression):
    def __init__(self, test, body):
        super(WhileStatement, self).__init__(
            type=Syntax.WhileStatement,
            test=test,
            body=body,
        )


class WithStatement(Expression):
    def __init__(self, object, body):
        super(WithStatement, self).__init__(
            type=Syntax.WithStatement,
            object=object,
            body=body,
        )


class YieldExpression(Expression):
    def __init__(self, argument, delegate):
        super(YieldExpression, self).__init__(
            type=Syntax.YieldExpression,
            argument=argument,
            delegate=delegate,
        )
