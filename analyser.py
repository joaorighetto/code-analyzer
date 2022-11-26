import ast
from pprint import pprint
import re


class Analyser(ast.NodeVisitor):
    def __init__(self):
        self.analysed = {"attributes": [], "arguments": [], "func_names": [], "warnings": []}

    def visit_FunctionDef(self, node):
        for a in node.args.args:
            args = (a.arg, a.lineno, node.col_offset, node.end_col_offset, "Argumento de funcao")
            self.analysed["arguments"].append(args)
        names = (node.name, node.lineno, node.col_offset, node.end_col_offset, "Nome de funcao")
        self.analysed["func_names"].append(names)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        attrs = (node.attr, node.lineno, node.col_offset, node.end_col_offset, "Atributos")
        self.analysed["attributes"].append(attrs)

    def visit_Name(self, node):
        args = (node.id, node.lineno, node.col_offset, node.end_col_offset, "Nomes")
        self.analysed["arguments"].append(args)

    def check_camel_case(self):  # S010 & S012 checks
        for tup in self.analysed["arguments"]:
            if not re.match(r"^_{0,2}[\da-z_]+", tup[0]):
                snake_case_warning = f"Line {tup[1]}: S010 Argument name '{tup[0]}' should be snake_case"
                if snake_case_warning not in self.analysed["warnings"]:
                    self.analysed["warnings"].append(snake_case_warning)
        for tup in self.analysed["attributes"]:
            if not re.match(r"^_{0,2}[\da-z_]+", tup[0]):
                snake_case_warning = f"Line {tup[1]}: S011 Variable '{tup[0]}' should be snake_case"
                if snake_case_warning not in self.analysed["warnings"]:
                    self.analysed["warnings"].append(snake_case_warning)
        for tup in self.analysed["func_names"]:
            if not re.match(r"^_{0,2}[\da-z_]+", tup[0]):
                snake_case_warning = f"Line {tup[1]}: S011 Variable '{tup[0]}' should be snake_case"
                if snake_case_warning not in self.analysed["warnings"]:
                    self.analysed["warnings"].append(snake_case_warning)

    def report(self):
        pprint(self.analysed)
