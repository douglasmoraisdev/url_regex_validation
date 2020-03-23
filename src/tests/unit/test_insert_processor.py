#!/usr/bin/env python3
import unittest
from unittest.mock import MagicMock
from rabbitmq_admin import AdminAPI

from core.insert_processor import InsertProcessor
from services.rabbitmq import RabbitmqService
from models.client_whitelist import ClientWhitelistModel
from models.global_whitelist import GlobalWhitelistModel

from os import environ
from dotenv import load_dotenv


class TestInsertionProcessor(unittest.TestCase):

    def setUp(self):
        load_dotenv(dotenv_path='tests/.env', override=True)

        self.rabbitmq_api = AdminAPI(url="http://%s:%s" % (environ.get('RABBITMQ_URL'), environ.get('RABBITMQ_API_PORT')),
                                     auth=(environ.get('RABBITMQ_USER'),
                                           environ.get('RABBITMQ_PASSWORD')))

        self.rabbitmq_api.create_vhost(environ.get('RABBITMQ_VHOST'))

        self.broker = RabbitmqService()

    def test_insertion_process_client(self):

        regex = '^(https:\\/\\/)?(www.|m.)?facebook\\.com(.br)?(\\/|\\/\\w+)?$'
        payload = {"client": "facebook", 
                    "regex": regex}

        client_model = ClientWhitelistModel()
        global_model = GlobalWhitelistModel()

        client_model.insert_client_regex = MagicMock(return_value=True)
        global_model.insert_global_regex = MagicMock(return_value=True)

        insert_processor = InsertProcessor(self.broker, client_model, global_model)
        process_result = insert_processor.process(payload)
        
        self.assertTrue(process_result)
        self.assertIn('facebook', client_model.insert_client_regex.call_args[0][0])
        self.assertIn(regex, client_model.insert_client_regex.call_args[0][1])
        self.assertEqual(client_model.insert_client_regex.call_count, 1)
        self.assertEqual(global_model.insert_global_regex.call_count, 0)

    def test_insertion_process_global(self):

        regex = '^(https:\\/\\/)?(www.|m.)?facebook\\.com(.br)?(\\/|\\/\\w+)?$'
        payload = {"client": "", 
                    "regex": regex}

        client_model = ClientWhitelistModel()
        global_model = GlobalWhitelistModel()

        client_model.insert_client_regex = MagicMock(return_value=True)
        global_model.insert_global_regex = MagicMock(return_value=True)

        insert_processor = InsertProcessor(self.broker, client_model, global_model)
        process_result = insert_processor.process(payload)
        
        self.assertTrue(process_result)
        self.assertIn(regex, global_model.insert_global_regex.call_args[0][0])
        self.assertEqual(client_model.insert_client_regex.call_count, 0)
        self.assertEqual(global_model.insert_global_regex.call_count, 1)

    def test_insertion_invalid_payload(self):

        regex = '^(https:\\/\\/)?(www.|m.)?facebook\\.com(.br)?(\\/|\\/\\w+)?$'
        payload = {"key_unknow": "foo_bar", 
                    "regex": regex}

        client_model = ClientWhitelistModel()
        global_model = GlobalWhitelistModel()

        client_model.insert_client_regex = MagicMock(return_value=True)
        global_model.insert_global_regex = MagicMock(return_value=True)

        insert_processor = InsertProcessor(self.broker, client_model, global_model)
        process_result = insert_processor.process(payload)
        
        self.assertEqual(client_model.insert_client_regex.call_count, 0)
        self.assertEqual(global_model.insert_global_regex.call_count, 0)

    def test_insertion_invalid_regex(self):

        regex = '^(https:anithingbut_regex:$'
        payload = {"client": "facebook", 
                    "regex": regex}

        client_model = ClientWhitelistModel()
        global_model = GlobalWhitelistModel()

        client_model.insert_client_regex = MagicMock(return_value=True)
        global_model.insert_global_regex = MagicMock(return_value=True)

        insert_processor = InsertProcessor(self.broker, client_model, global_model)
        process_result = insert_processor.process(payload)
        
        self.assertEqual(client_model.insert_client_regex.call_count, 0)
        self.assertEqual(global_model.insert_global_regex.call_count, 0)

    def tearDown(self):
        self.rabbitmq_api.delete_vhost(environ.get('RABBITMQ_VHOST'))

if __name__ == '__main__':
    unittest.main()
