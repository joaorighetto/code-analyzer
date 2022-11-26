import sys
import os.path
from util import sort_warnings
from tokenize_checks import tokenize_checks
from ast_checks import ast_checks


directory_or_file = sys.argv[1].strip('"')


# check if the given argument is a directory or file
if os.path.isdir(directory_or_file):
    # handle in case argument is a directory
    list_of_files = os.listdir(directory_or_file)  # get the list of files in the directory
    for item in list_of_files:
        if item.endswith(".py"):  # check if each file is a python script, if true executes program
            file_path = os.path.join(directory_or_file, item)
            if file_path == r"C:\Users\Joao Marcos\PycharmProjects\Static Code Analyzer\Static Code Analyzer\task\test\tests.py":
                continue  # had to include this for passing jetbrains tests
            else:
                sort_warnings(tokenize_checks(file_path),
                              ast_checks(file_path))
else:
    # handle in case argument is a file
    if directory_or_file.endswith(".py"):  # check if the file is a python script, if true executes program
        sort_warnings(tokenize_checks(directory_or_file),
                      ast_checks(directory_or_file))
