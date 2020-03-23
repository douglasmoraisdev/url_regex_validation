from utils import regex_utils


class WhitelistMatcher:

    def __init__(self, model):

        self.model = model

    def get_match(self, **args) -> str:
        whitelist = self.model.get_whitelist(args)

        for whitelist_item in whitelist:
            if regex_utils.is_match_regex(whitelist_item.regex, args['url']):
                return whitelist_item.regex

        return ""
