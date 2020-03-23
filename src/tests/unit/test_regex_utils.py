#!/usr/bin/env python3
import unittest
from utils import regex_utils


class TestValidationRegex(unittest.TestCase):

    def test_is_match(self):

        regex = "^(https:\\/\\/)?(www.|m.)?instagram\\.com(.br)?(\\/|\\/\\w+)?$"

        url = "m.instagram.com"
        self.assertTrue(regex_utils.is_match_regex(regex, url))

        url = "www.instagram.com"
        self.assertTrue(regex_utils.is_match_regex(regex, url))

        url = "www.instagram.com.br"
        self.assertTrue(regex_utils.is_match_regex(regex, url))

        url = "https://www.instagram.com/login"
        self.assertTrue(regex_utils.is_match_regex(regex, url))

        url = "https://instagram.com"
        self.assertTrue(regex_utils.is_match_regex(regex, url))

    def test_not_match(self):

        regex = "^(https:\/\/)?(www.|m.)?instagram\.com(.br)?(\/|\/\w+)?$"

        url = "m.facebook.com"
        self.assertFalse(regex_utils.is_match_regex(regex, url))

        url = "www.instagram.comu"
        self.assertFalse(regex_utils.is_match_regex(regex, url))

        url = "www.instagram.br"
        self.assertFalse(regex_utils.is_match_regex(regex, url))

        url = "https://fake.instagram.com/login"
        self.assertFalse(regex_utils.is_match_regex(regex, url))

        url = "https://hackininstagram.com/login"
        self.assertFalse(regex_utils.is_match_regex(regex, url))

    def test_is_valid_regex_true(self):

        regex = "^(https:\\/\\/)?(www.|m.)?facebook\\.com(.br)?(\\/|\\/\\w+)?$"

        self.assertTrue(regex_utils.is_valid_regex(regex))

    def test_is_valid_regex_false(self):

        regex = "^(https:anithingbut_regex:$"

        self.assertFalse(regex_utils.is_valid_regex(regex))


if __name__ == '__main__':
    unittest.main()
