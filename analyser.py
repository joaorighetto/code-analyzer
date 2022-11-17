import ast
from pprint import pprint


class Analyser(ast.NodeVisitor):
    def __init__(self):
        self.analysed = {"arguments": []}

    def visit_FunctionDef(self, node):
        """ Visit all function definitions in the tree and extract their arguments and line numbers. """

        args = [(a.arg, a.lineno) for a in node.args.args]
        self.analysed["arguments"].append(args)
        self.generic_visit(node)

    def visit_Assign(self, node):
        pass

    def report(self):
        pprint(self.analysed)
