import os.path
import sys
import ast
import re
import tokenize


def perform_checks(tree, path):
    warnings = []
    for step in ast.walk(tree):
        if isinstance(step, ast.FunctionDef):
            argument_names = [a.arg for a in step.args.args]
            for argument in argument_names:
                if not re.match(r"^_{0,2}[\da-z_]+", argument):
                    snake_case_warning = f"{path}: Line {step.lineno}: S010 Argument name '{argument}' should be snake_case"
                    if snake_case_warning not in warnings:
                        warnings.append(snake_case_warning)
            for elem in step.args.defaults:
                if isinstance(elem, ast.List):
                    mutable_argument_warning = f"{path}: Line {elem.lineno}: S012 Default argument value is mutable"
                    warnings.append(mutable_argument_warning)
        elif isinstance(step, ast.Name) and isinstance(step.ctx, ast.Store):
            variable = step.id
            if not re.match(r"^_{0,2}[\da-z_]+", variable):
                snake_case_warning = f"{path}: Line {step.lineno}: S011 Variable '{variable}' should be snake_case"
                if snake_case_warning not in warnings:
                    warnings.append(snake_case_warning)

    return warnings


def ast_checks(path):
    with open(path, "r") as file:
        tree = ast.parse(file.read())
        warnings = perform_checks(tree, path)
        return warnings


def tokenize_checks(path):

    warnings = []
    with open(path, "r") as file:
        new_line_count = 0
        for toktype, tok, start, end, line in tokenize.generate_tokens(file.readline):

            if len(line) > 79 and f"{path}: Line {start[0]}: S001 Too long" not in warnings:
                warnings.append(f"{path}: Line {start[0]}: S001 Too long")

            if (len(line) - len(line.lstrip(" "))) % 4 != 0 and f"{path}: Line {start[0]}: S002 Indentation is not a multiple of four" not in warnings:
                warnings.append(f"{path}: Line {start[0]}: S002 Indentation is not a multiple of four")

            if toktype != tokenize.COMMENT and tok.endswith(";"):
                if f"{path}: Line {start[0]}: S003 Unnecessary semicolon" not in warnings:
                    warnings.append(f"{path}: Line {start[0]}: S003 Unnecessary semicolon")

            if toktype == tokenize.COMMENT:
                lower_tok = tok.casefold()
                if "todo" in lower_tok:
                    warnings.append(f"{path}: Line {start[0]}: S005 TODO found")

                if line.startswith("#"):
                    continue
                if len(line[:start[1]]) - len(line[:start[1]].rstrip()) != 2:
                    warnings.append(f"{path}: Line {start[0]}: S004 At least two spaces required before inline comments")

            if toktype == tokenize.NEWLINE or toktype == tokenize.NL:
                new_line_count += 1
                if new_line_count == 4:
                    warnings.append(f"{path}: Line {start[0] + 1}: S006 More than two blank lines used before this line")
                    new_line_count = 0
                    continue
            else:
                new_line_count = 0

            template_1 = r"_{0,2}def {2,}\w|class {2,}\w"  # template match if there's 2 or more spaces between the keywords 'def' or 'class' and their name definition
            if "class" in line or "def" in line:
                line = line.lstrip()
                if line.startswith("class") or line.startswith("def"):
                    if toktype == tokenize.NAME and tok == "class" or tok == "def":
                        if re.match(template_1, line):
                            warnings.append(f"{path}: Line {start[0]}: S007 Too many spaces after '{tok}'")

            template_2 = r"[A-Z][a-z]*([A-Z][a-z]*)|[A-Z]\w+"  # template match PascalCase words(""CamelCase"" for jetbrains)
            if "class" in line:
                line = line.lstrip()
                if line.startswith("class"):
                    if toktype == tokenize.NAME and tok != "class":
                        if not re.match(template_2, tok):
                            warnings.append(f"{path}: Line {start[0]}: S008  Class name '{tok}' should use CamelCase")

            template_3 = r"def _{1,2}[0-9a-z_]*|def [^_A-Z][0-9a-z_]*"
            if "def" in line:
                line = line.lstrip()
                if line.startswith("def"):
                    if toktype == tokenize.NAME and tok != "def":
                        if not re.match(template_3, line):
                            warnings.append(f"{path}: Line {start[0]}: S009 Function name '{tok}' should use snake_case")
    return warnings


def convert(s):
    """Convert a string to int if possible, if not return the string unchanged."""
    return int(s) if s.isdigit() else s


def alphanum(text):
    """Transform a string into a list of string and int chunks."""
    return [convert(chunk) for chunk in re.split(r'(\d+)', text)]


def sort_warnings(*warnings):
    warnings_list = []
    for warning in warnings:
        warnings_list += warning
    warnings_list.sort(key=alphanum)
    for warning in warnings_list:
        print(warning)


directory_or_file = sys.argv[1].strip('"')


# check if the given argument is a directory or file
if os.path.isdir(directory_or_file):
    # handle in case argument is a directory
    list_of_files = os.listdir(directory_or_file)  # get the list of files in the directory
    for item in list_of_files:
        if item.endswith(".py"):  # check if each file is a python script, if true executes program
            file_path = os.path.join(directory_or_file, item)
            sort_warnings(tokenize_checks(file_path),
                          ast_checks(file_path))
else:
    # handle in case argument is a file
    if directory_or_file.endswith(".py"):  # check if the file is a python script, if true executes program
        sort_warnings(tokenize_checks(directory_or_file),
                      ast_checks(directory_or_file))
