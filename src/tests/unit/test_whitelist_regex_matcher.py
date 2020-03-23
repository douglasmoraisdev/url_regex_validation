#!/usr/bin/env python3
import unittest
from unittest.mock import MagicMock

from collections import namedtuple

from core.url_matcher import UrlMatcher

from core.whitelist_matcher import WhitelistMatcher

from models.client_whitelist import ClientWhitelistModel
from models.global_whitelist import GlobalWhitelistModel


class TestWhitelistMatch(unittest.TestCase):

    def setUp(self):
        self.whiteliststruct = namedtuple('whitelist', 'regex')

    def test_validator_only_client_url(self):

        validation_regex = "^(https:\/\/)?(www.|m.)?instagram\.com(.br)?(\/|\/\w+)?$"
        no_validator_regex = "^(https:\/\/)?(www.|m.)?twitter\.com(.br)?(\/|\/\w+)?$"

        client_whitelist = self.whiteliststruct(regex=validation_regex)
        global_whitelist = self.whiteliststruct(regex=no_validator_regex) 
        url = 'm.instagram.com/login'
        client = 'instagram'

        client_model = ClientWhitelistModel()
        global_model = GlobalWhitelistModel()

        client_model.get_whitelist = MagicMock(return_value=[client_whitelist])
        global_model.get_whitelist = MagicMock(return_value=[global_whitelist])

        client_validator = WhitelistMatcher(client_model)
        global_validator = WhitelistMatcher(global_model)

        match = client_validator.get_match(client=client, url=url)

        self.assertEqual(match, validation_regex)
        self.assertEqual(client_model.get_whitelist.call_count, 1)
        self.assertEqual(global_model.get_whitelist.call_count, 0)
        self.assertIn('client', client_model.get_whitelist.call_args[0][0])
        self.assertIn('url', client_model.get_whitelist.call_args[0][0])

    def test_validator_only_global_url(self):

        validation_regex = "^(https:\/\/)?(www.|m.)?instagram\.com(.br)?(\/|\/\w+)?$"
        no_validator_regex = "^(https:\/\/)?(www.|m.)?twitter\.com(.br)?(\/|\/\w+)?$"

        client_whitelist = self.whiteliststruct(regex=no_validator_regex)
        global_whitelist = self.whiteliststruct(regex=validation_regex) 
        url = 'm.instagram.com/login'
        client = ''

        client_model = ClientWhitelistModel()
        global_model = GlobalWhitelistModel()

        client_model.get_whitelist = MagicMock(return_value=[client_whitelist])
        global_model.get_whitelist = MagicMock(return_value=[global_whitelist])

        client_validator = WhitelistMatcher(client_model)
        global_validator = WhitelistMatcher(global_model)

        match = global_validator.get_match(client=client, url=url)

        self.assertEqual(match, validation_regex)
        self.assertEqual(client_model.get_whitelist.call_count, 0)
        self.assertEqual(global_model.get_whitelist.call_count, 1)
        self.assertIn('url', global_model.get_whitelist.call_args[0][0])