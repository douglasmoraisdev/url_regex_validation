#!/usr/bin/env python3
import unittest
from unittest.mock import MagicMock
from utils.rabbitmq_utils import RabbitmqCallback


class TestRabbitmqUtils(unittest.TestCase):

    def setUp(self):
        def mock_callable(**args):
            return args

        self.mock_callable = mock_callable

    def test_callback_body_call(self):

        callback_target = self.mock_callable
        callback_target = MagicMock(return_value=True)
        rabbitmq = RabbitmqCallback(callback_target)

        ch, method, parameters = 'not', 'in', 'use'
        body = b'{"client": "facebook", "regex": "^(https:\\/\\/)?(www.|m.)?facebook\\.com(.br)?(\\/|\\/\\w+)?$"}'

        rabbitmq.callback_dict_body(ch, method, parameters, body)

        self.assertEqual(callback_target.call_count, 1)
        self.assertIsInstance(callback_target.call_args[0][0], dict)
        self.assertIn('client', callback_target.call_args[0][0])
        self.assertIn('regex', callback_target.call_args[0][0])
        self.assertEqual(callback_target.call_args[0][0]['client'], 'facebook')
        self.assertEqual(callback_target.call_args[0][0]['regex'], "^(https:\\/\\/)?(www.|m.)?facebook\\.com(.br)?(\\/|\\/\\w+)?$")

    def test_format_dict_body_valid_payload(self):

        callback_target = self.mock_callable
        callback_target = MagicMock(return_value=True)
        rabbitmq = RabbitmqCallback(callback_target)

        body = b'{"client": "facebook", "regex": "^(https:\\/\\/)?(www.|m.)?facebook\\.com(.br)?(\\/|\\/\\w+)?$"}'

        formated_dict = rabbitmq._format_payload_to_dict(body)

        self.assertIsInstance(formated_dict, dict)
        self.assertEqual(len(formated_dict), 2)
        self.assertEqual(formated_dict['client'], 'facebook')
        self.assertEqual(formated_dict['regex'], "^(https:\\/\\/)?(www.|m.)?facebook\\.com(.br)?(\\/|\\/\\w+)?$")

    def test_format_dict_body_invalid_payload(self):

        callback_target = self.mock_callable
        callback_target = MagicMock(return_value=True)
        rabbitmq = RabbitmqCallback(callback_target)

        body = b'{some fuzzy non json/dict payload]'

        with self.assertRaises(SyntaxError):
            rabbitmq._format_payload_to_dict(body)

if __name__ == '__main__':
    unittest.main()
