import ast
from pprint import pprint


class Analyser(ast.NodeVisitor):
    def __init__(self):
        self.analysed = {"attributes": [], "arguments": [], "names": []}

    def visit_FunctionDef(self, node):
        """ Visit all function definitions in the tree and extract their arguments and line numbers. """

        args = [(a.arg, a.lineno) for a in node.args.args]
        self.analysed["arguments"].append(args)
        self.analysed["names"].append((node.name, node.lineno))
        self.generic_visit(node)

    def visit_Name(self, node):
        self.analysed["names"].append((node.id, node.lineno))
        self.generic_visit(node)

    def visit_Attribute(self, node):
        self.analysed["attributes"].append((node.attr, node.lineno))
        self.generic_visit(node)


    def report(self):
        pprint(self.analysed)
