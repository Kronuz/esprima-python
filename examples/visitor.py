from __future__ import print_function

import json
import esprima

# Build a CallExpression expression statement manually:
callee = esprima.nodes.Identifier("alert")
args = [esprima.nodes.Literal("other alert", "'other alert'")]
call = esprima.nodes.CallExpression(callee, args)
other_alert = esprima.nodes.ExpressionStatement(call)

# Add a few expression statements using `parse()`:
expression_statements = {
    'some_alert': esprima.parse("alert('some alert')").body[0],
    'other_alert': other_alert,
    'console_log': esprima.parse("console.log()").body[0],
}


class MyVisitor(esprima.NodeVisitor):
    def transform_CallExpression(self, node, metadata):
        # If the callee is an `alert()`, change it to `console.log()`:
        if node.callee.name == 'alert':
            new_node = expression_statements['console_log'].expression
            new_node.arguments = node.arguments
            node = new_node
        return self.generic_transform(node, metadata)

    def visit_BlockStatement(self, node):
        # Add the expression statements to the body:
        node.body.append(expression_statements['some_alert'])

        node.body.append(expression_statements['other_alert'])

        # Make sure everything else gets visited:
        self.generic_visit(node)


visitor = MyVisitor()


tree = esprima.parse("""
alert('first alert');
function foo() {
    var i2= 20;
    alert('foo function');
}
""", delegate=visitor)

visitor.visit(tree)

print(json.dumps(tree.toDict(), indent=2))
