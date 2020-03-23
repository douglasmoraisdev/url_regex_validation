#!/usr/bin/env python3
import unittest
from unittest.mock import MagicMock
from rabbitmq_admin import AdminAPI

from core.url_matcher import UrlMatcher
from core.match_processor import MatchProcessor
from services.rabbitmq import RabbitmqService

from os import environ
from dotenv import load_dotenv


class TestMatchProcessor(unittest.TestCase):

    def setUp(self):
        load_dotenv(dotenv_path='tests/.env', override=True)

        self.rabbitmq_api = AdminAPI(url="http://%s:%s" % (environ.get('RABBITMQ_URL'), environ.get('RABBITMQ_API_PORT')),
                                     auth=(environ.get('RABBITMQ_USER'),
                                           environ.get('RABBITMQ_PASSWORD')))

        self.rabbitmq_api.create_vhost(environ.get('RABBITMQ_VHOST'))

        self.broker = RabbitmqService()
        self.broker.post = MagicMock(return_value=True)

    def test_process_url_validation_true(self):

        correlationId = 'abcd-1234'
        payload = {"client": "facebook",
                   "url": "http://www.instagram.com/login",
                   "correlationId": "%s" % correlationId
                   }
        regex = '^(https:\/\/)?(www.|m.)?instagram\.com(.br)?(\/|\/\w+)?$'

        url_matcher = UrlMatcher('', '')
        url_matcher.match_url = MagicMock(return_value=regex)

        match_processor = MatchProcessor(self.broker, url_matcher)

        process_result = match_processor.process(payload)

        self.assertEqual(
            self.broker.post.call_args[0][0], u"{'regex': '^(https:\\/\\/)?(www.|m.)?instagram\\.com(.br)?(\\/|\\/\\w+)?$', 'validation': True, 'correlationId': 'abcd-1234'}")

    def test_process_url_validation_false(self):

        correlationId = 'abcd-1234'
        payload = {"client": "facebook",
                   "url": "http://www.instagram.com/login",
                   "correlationId": "%s" % correlationId
                   }

        url_matcher = UrlMatcher('', '')
        url_matcher.match_url = MagicMock(return_value='')

        match_processor = MatchProcessor(self.broker, url_matcher)

        process_result = match_processor.process(payload)

        self.assertEqual(self.broker.post.call_count, 1)
        self.assertEqual(
            self.broker.post.call_args[0][0], "{'regex': 'null', 'validation': False, 'correlationId': 'abcd-1234'}")

    def test_process_invalid_payload(self):

        correlationId = 'abcd-1234'
        payload = {"timestamp": "some-timestamp",
                   "client": "facebook",
                   "random-key": "%s" % correlationId
                   }

        url_matcher = UrlMatcher('', '')
        url_matcher.match_url = MagicMock(return_value='')

        match_processor = MatchProcessor(self.broker, url_matcher)

        process_result = match_processor.process(payload)

        self.assertEqual(self.broker.post.call_count, 0)

    def test_process_invalid_url(self):

        correlationId = 'abcd-1234'
        payload = {"client": "facebook",
                   "url": "123://hackininstagram.com/login",
                   "correlationId": "%s" % correlationId
                   }

        url_matcher = UrlMatcher('', '')
        url_matcher.match_url = MagicMock(return_value='')

        match_processor = MatchProcessor(self.broker, url_matcher)

        process_result = match_processor.process(payload)

        self.assertEqual(self.broker.post.call_count, 0)

    def test_process_invalid_correlationId(self):

        payload = {"client": "facebook",
                   "url": "http://www.instagram.com/login",
                   "correlationId": ""
                   }

        url_matcher = UrlMatcher('', '')
        url_matcher.match_url = MagicMock(return_value='')

        match_processor = MatchProcessor(self.broker, url_matcher)

        process_result = match_processor.process(payload)

        self.assertEqual(self.broker.post.call_count, 0)

    def tearDown(self):
        self.rabbitmq_api.delete_vhost(environ.get('RABBITMQ_VHOST'))

if __name__ == '__main__':
    unittest.main()
