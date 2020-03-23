#!/usr/bin/env python3
import unittest
from unittest.mock import MagicMock

from collections import namedtuple

from core.url_matcher import UrlMatcher

from core.whitelist_matcher import WhitelistMatcher

from models.client_whitelist import ClientWhitelistModel
from models.global_whitelist import GlobalWhitelistModel


class TestUrlMatcher(unittest.TestCase):

    def setUp(self):
        self.whiteliststruct = namedtuple('whitelist', 'regex')

        self.client_model = ClientWhitelistModel()
        self.global_model = GlobalWhitelistModel()

    def test_validator_only_client_url(self):

        validation_regex = "^(https:\/\/)?(www.|m.)?instagram\.com(.br)?(\/|\/\w+)?$"
        no_validator_regex = "^(https:\/\/)?(www.|m.)?twitter\.com(.br)?(\/|\/\w+)?$"

        client_whitelist = self.whiteliststruct(regex=validation_regex)
        global_whitelist = self.whiteliststruct(regex=no_validator_regex) 
        url = 'm.instagram.com/login'
        client = 'instagram'

        self.client_model.get_whitelist = MagicMock(return_value=[client_whitelist])
        self.global_model.get_whitelist = MagicMock(return_value=[global_whitelist])

        client_matcher = WhitelistMatcher(self.client_model)
        global_matcher = WhitelistMatcher(self.global_model)

        url_matcher = UrlMatcher(client_matcher, global_matcher)

        result = url_matcher.match_url(url, client)

        self.assertIsInstance(result, str)
        self.assertEqual(validation_regex, result)

    def test_validator_only_global_url(self):

        validation_regex = "^(https:\/\/)?(www.|m.)?twitter\.com(.br)?(\/|\/\w+)?$"
        no_validator_regex = "^(https:\/\/)?(www.|m.)?instagram\.com(.br)?(\/|\/\w+)?$"

        client_whitelist = self.whiteliststruct(regex=no_validator_regex)
        global_whitelist = self.whiteliststruct(regex=validation_regex)        
        url = 'www.twitter.com'
        client = ''

        self.client_model.get_whitelist = MagicMock(return_value=[client_whitelist])
        self.global_model.get_whitelist = MagicMock(return_value=[global_whitelist])

        client_matcher = WhitelistMatcher(self.client_model)
        global_matcher = WhitelistMatcher(self.global_model)
        
        url_matcher = UrlMatcher(client_matcher, global_matcher)

        result = url_matcher.match_url(url, client)

        self.assertIsInstance(result, str)
        self.assertEqual(validation_regex, result)

    def test_validator_global_and_client_url(self):

        validation_regex = "^(https:\/\/)?(www.|m.)?facebook\.com(.br)?(\/|\/\w+)?$"

        client_whitelist = self.whiteliststruct(regex=validation_regex)
        global_whitelist = self.whiteliststruct(regex=validation_regex)
        url = 'facebook.com'
        client = 'facebook'

        self.client_model.get_whitelist = MagicMock(
            return_value=[client_whitelist])
        self.global_model.get_whitelist = MagicMock(
            return_value=[global_whitelist])

        client_matcher = WhitelistMatcher(self.client_model)
        global_matcher = WhitelistMatcher(self.global_model)

        url_matcher = UrlMatcher(client_matcher, global_matcher)

        result = url_matcher.match_url(url, client)

        self.assertIsInstance(result, str)
        self.assertEqual(validation_regex, result)

    def test_no_validator_global_and_client_url(self):

        no_validator_regex_a = "^(https:\/\/)?(www.|m.)?instagram\.com(.br)?(\/|\/\w+)?$"
        no_validator_regex_b = "^(https:\/\/)?(www.|m.)?facebook\.com(.br)?(\/|\/\w+)?$"

        client_whitelist = self.whiteliststruct(regex=no_validator_regex_a)
        global_whitelist = self.whiteliststruct(regex=no_validator_regex_b)
        url = 'www.twitter.com'
        client = ''

        self.client_model.get_whitelist = MagicMock(
            return_value=[client_whitelist])
        self.global_model.get_whitelist = MagicMock(
            return_value=[global_whitelist])

        client_matcher = WhitelistMatcher(self.client_model)
        global_matcher = WhitelistMatcher(self.global_model)

        url_matcher = UrlMatcher(client_matcher, global_matcher)

        result = url_matcher.match_url(url, client)

        self.assertIsInstance(result, str)
        self.assertEqual(result, "")

if __name__ == '__main__':
    unittest.main()
