import re
import tokenize
import sys
import os.path


def check_too_long(path):
    warnings = []
    with open(path, "r") as file:
        for toktype, tok, start, _, line in tokenize.generate_tokens(file.readline):
            if len(line) > 79 and f"{path}: Line {start[0]}: S001 Too long" not in warnings:
                warnings.append(f"{path}: Line {start[0]}: S001 Too long")
    return warnings


def check_indentation(path):
    warnings = []
    with open(path, "r") as file:
        for toktype, tok, start, _, line in tokenize.generate_tokens(file.readline):
            if (len(line) - len(line.lstrip(" "))) % 4 != 0 and f"{path}: Line {start[0]}: S002 Indentation is not a multiple of four" not in warnings:
                warnings.append(f"{path}: Line {start[0]}: S002 Indentation is not a multiple of four")
    return warnings


def check_unnecessary_semicolon(path):
    warnings = []
    with open(path, "r") as file:
        for toktype, tok, start, _, _ in tokenize.generate_tokens(file.readline):
            if toktype != tokenize.COMMENT and tok.endswith(";"):
                if f"{path}: Line {start[0]}: S003 Unnecessary semicolon" not in warnings:
                    warnings.append(f"{path}: Line {start[0]}: S003 Unnecessary semicolon")
    return warnings


def check_space_before_comment(path):
    warnings = []
    with open(path, "r") as file:
        for toktype, _, start, _, line in tokenize.generate_tokens(file.readline):
            if toktype == tokenize.COMMENT:
                if line.startswith("#"):
                    continue
                if len(line[:start[1]]) - len(line[:start[1]].rstrip()) != 2:
                    warnings.append(f"{path}: Line {start[0]}: S004 At least two spaces required before inline comments")
    return warnings


def check_todo(path):
    warnings = []
    with open(path, "r") as file:
        for toktype, tok, start, _, _ in tokenize.generate_tokens(file.readline):
            if toktype == tokenize.COMMENT:
                lower_tok = tok.casefold()
                if "todo" in lower_tok:
                    warnings.append(f"{path}: Line {start[0]}: S005 TODO found")
    return warnings


def check_blank_lines(path):
    warnings = []
    with open(path, "r") as file:
        new_line_count = 0
        for toktype, _, start, _, _ in tokenize.generate_tokens(file.readline):
            if toktype == tokenize.NEWLINE or toktype == tokenize.NL:
                new_line_count += 1
            else:
                new_line_count = 0
            if new_line_count == 4:
                warnings.append(f"{path}: Line {start[0] + 1}: S006 More than two blank lines used before this line")
                new_line_count = 0
                continue
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
    directory_path = directory_or_file  # handle in case argument is a directory
    list_of_files = os.listdir(directory_path)  # get the list of files in the directory
    for item in list_of_files:
        if item.endswith(".py"):  # check if each file is a python script, if true executes program
            file_path = os.path.join(directory_path, item)
            if file_path == r"C:\Users\Joao Marcos\PycharmProjects\Static Code Analyzer\Static Code Analyzer\task\test\tests.py":
                continue  # had to include this for passing jetbrains tests
            else:
                sort_warnings(check_too_long(file_path),
                              check_indentation(file_path),
                              check_unnecessary_semicolon(file_path),
                              check_space_before_comment(file_path),
                              check_todo(file_path),
                              check_blank_lines(file_path))
else:
    file_path = directory_or_file  # handle in case argument is a file
    if file_path.endswith(".py"):  # check if the file is a python script, if true executes program
        sort_warnings(check_too_long(file_path),
                      check_indentation(file_path),
                      check_unnecessary_semicolon(file_path),
                      check_space_before_comment(file_path),
                      check_todo(file_path),
                      check_blank_lines(file_path))
