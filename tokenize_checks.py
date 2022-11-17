import tokenize
import re


def tokenize_checks(path):
    warnings = []
    # new_line_count = 0
    # with open(path, "r") as file:
    #     for toktype, tok, start, end, line in tokenize.generate_tokens(file.readline):
    #
    #         if len(line) > 79 and f"{path}: Line {start[0]}: S001 Too long" not in warnings:
    #             warnings.append(f"{path}: Line {start[0]}: S001 Too long")
    #
    #         if (len(line) - len(line.lstrip(" "))) % 4 != 0 and f"{path}: Line {start[0]}: S002 Indentation is not a multiple of four" not in warnings:
    #             warnings.append(f"{path}: Line {start[0]}: S002 Indentation is not a multiple of four")
    #
    #         if toktype != tokenize.COMMENT and tok.endswith(";"):
    #             if f"{path}: Line {start[0]}: S003 Unnecessary semicolon" not in warnings:
    #                 warnings.append(f"{path}: Line {start[0]}: S003 Unnecessary semicolon")
    #
    #         if toktype == tokenize.COMMENT:
    #             lower_tok = tok.casefold()
    #             if "todo" in lower_tok:
    #                 warnings.append(f"{path}: Line {start[0]}: S005 TODO found")
    #
    #             if line.startswith("#"):
    #                 continue
    #             if len(line[:start[1]]) - len(line[:start[1]].rstrip()) != 2:
    #                 warnings.append(f"{path}: Line {start[0]}: S004 At least two spaces required before inline comments")
    #
    #         if toktype == tokenize.NEWLINE or toktype == tokenize.NL:
    #             new_line_count += 1
    #         else:
    #             new_line_count = 0
    #             if new_line_count == 4:
    #                 warnings.append(f"{path}: Line {start[0] + 1}: S006 More than two blank lines used before this line")
    #                 new_line_count = 0
    #                 continue
    #
    #         template_1 = r"_{0,2}def {2,}\w|class {2,}\w"  # template match if there's 2 or more spaces between the keywords 'def' or 'class' and their name definition
    #         if "class" in line or "def" in line:
    #             line = line.lstrip()
    #             if line.startswith("class") or line.startswith("def"):
    #                 if toktype == tokenize.NAME and tok == "class" or tok == "def":
    #                     if re.match(template_1, line):
    #                         warnings.append(f"{path}: Line {start[0]}: S007 Too many spaces after '{tok}'")
    #
    #         template_2 = r"[A-Z][a-z]*([A-Z][a-z]*)|[A-Z]\w+"  # template match PascalCase words(""CamelCase"" for jetbrains)
    #         if "class" in line:
    #             line = line.lstrip()
    #             if line.startswith("class"):
    #                 if toktype == tokenize.NAME and tok != "class":
    #                     if not re.match(template_2, tok):
    #                         warnings.append(f"{path}: Line {start[0]}: S008  Class name '{tok}' should use CamelCase")
    #
    #         template_3 = r"def _{2}[0-9a-z_]*|def [^_A-Z][0-9a-z_]*"
    #         if "def" in line:
    #             line = line.lstrip()
    #             if line.startswith("def"):
    #                 if toktype == tokenize.NAME and tok != "def":
    #                     if not re.match(template_3, line):
    #                         warnings.append(f"{path}: Line {start[0]}: S009 Function name '{tok}' should use snake_case")

    return warnings
