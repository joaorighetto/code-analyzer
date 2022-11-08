import re
import tokenize


def check_too_long(path):
    warnings = []
    with open(path, "r") as file:
        lines = file.readlines()
        line_count = 0
        for line in lines:
            line_count += 1
            if len(line) > 79:
                warnings.append(f"Line {line_count}: S001 Too long")
    return warnings


def check_indentation(path):
    warnings = []
    with open(path, "r") as file:
        lines = file.readlines()
    count_lines = 0
    for line in lines:
        count_lines += 1
        if line.startswith(" "):
            whitespace_count = 1
            while line[whitespace_count].isspace():
                whitespace_count += 1
            if whitespace_count % 4 != 0:
                warnings.append(f"Line {count_lines}: S002 Indentation is not a multiple of four")
        else:
            continue
    return warnings


def check_unnecessary_semicolon(path):
    warnings = []
    with open(path, "r") as file:
        for toktype, tok, start, _, _ in tokenize.generate_tokens(file.readline):
            if toktype != tokenize.COMMENT and tok.endswith(";"):
                if f"Line {start[0]}: S003 Unnecessary semicolon" not in warnings:
                    warnings.append(f"Line {start[0]}: S003 Unnecessary semicolon")
    return warnings


def check_space_before_comment(path):
    warnings = []
    with open(path, "r") as file:
        for toktype, _, start, _, line in tokenize.generate_tokens(file.readline):
            if toktype == tokenize.COMMENT:
                if line.startswith("#"):
                    continue
                if len(line[:start[1]]) - len(line[:start[1]].rstrip()) != 2:
                    warnings.append(f"Line {start[0]}: S004 At least two spaces required before inline comments")
    return warnings


def check_todo(path):
    warnings = []
    with open(path, "r") as file:
        for toktype, tok, start, _, _ in tokenize.generate_tokens(file.readline):
            if toktype == tokenize.COMMENT:
                lower_tok = tok.casefold()
                if "todo" in lower_tok:
                    warnings.append(f"Line {start[0]}: S005 TODO found")
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
                warnings.append(f"Line {start[0] + 1}: S006 More than two blank lines used before this line")
                new_line_count = 0
                continue
    return warnings


def convert(s):
    """
    Converts a string to int if possible, if not returns the string unchanged
    """
    return int(s) if s.isdigit() else s


def alphanum(text):
    """
    Transform a string into a list of string and int chunks.
    """
    return [convert(chunk) for chunk in re.split(r'(\d+)', text)]


def sort_warnings(*warnings):
    warnings_list = []
    for warning in warnings:
        warnings_list += warning
    warnings_list.sort(key=alphanum)
    for warning in warnings_list:
        print(warning)


file_path = input()
sort_warnings(check_too_long(file_path),
              check_indentation(file_path),
              check_unnecessary_semicolon(file_path),
              check_space_before_comment(file_path),
              check_todo(file_path),
              check_blank_lines(file_path))
