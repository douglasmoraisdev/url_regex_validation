#!/usr/bin/env python3
import unittest
from utils import url_utils


class TestUrlUtils(unittest.TestCase):

    def test_valid_url(self):

        url = "m.facebook.com"
        self.assertTrue(url_utils.is_valid_url(url))

        url = "www.instagram.comu"
        self.assertTrue(url_utils.is_valid_url(url))

        url = "www.instagram.br"
        self.assertTrue(url_utils.is_valid_url(url))

        url = "https://fake.instagram.com/login"
        self.assertTrue(url_utils.is_valid_url(url))

        url = "https://hackininstagram.com/login"
        self.assertTrue(url_utils.is_valid_url(url))


    def test_invalid_url(self):

        url = "/.facebook.com"
        self.assertFalse(url_utils.is_valid_url(url))

        url = "somecrazyur.."
        self.assertFalse(url_utils.is_valid_url(url))

        url = "www.;instagram.br"
        self.assertFalse(url_utils.is_valid_url(url))

        url = "tcp://fake.instagram.com/login"
        self.assertFalse(url_utils.is_valid_url(url))

        url = "123://hackininstagram.com/login"
        self.assertFalse(url_utils.is_valid_url(url))




if __name__ == '__main__':
    unittest.main()
