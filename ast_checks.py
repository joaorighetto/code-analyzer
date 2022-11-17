import ast
from analyser import Analyser


def ast_checks(path):
    warnings = []
    with open(path, "r") as file:
        tree = ast.parse(file.read())
        analyser = Analyser()
        analyser.visit(tree)
        analyser.report()
    return warnings
