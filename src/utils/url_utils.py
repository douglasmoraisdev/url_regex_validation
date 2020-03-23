import re

def is_valid_url(url):

    regex_url = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"

    return re.search(regex_url, url) is not None
