import re


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
