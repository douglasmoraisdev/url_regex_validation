import re


def is_match_regex(regex, payload):

    return re.search(regex, payload) is not None

def is_valid_regex(regex):

    try:
        re.compile(regex)
        is_compile = True
    except re.error:
        is_compile = False

    return is_compile