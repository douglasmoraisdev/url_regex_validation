#!/usr/bin/env python3
import unittest
from uuid import uuid4

import alembic.config
from sqlalchemy.orm import Session
from rabbitmq_admin import AdminAPI

from app import App

from services.rabbitmq import RabbitmqService

from core.url_matcher import UrlMatcher
from core.whitelist_matcher import WhitelistMatcher
from core.match_processor import MatchProcessor
from core.insert_processor import InsertProcessor
from core.flow import Flow

from utils.rabbitmq_utils import RabbitmqCallback

from models.client_whitelist import ClientWhitelistModel
from models.global_whitelist import GlobalWhitelistModel
from models.connectors.mysqldb import MySQLDBConnection

from os import environ
from dotenv import load_dotenv


class TestFlows(unittest.TestCase):

    def _setUpApplication(self):
        client_model = ClientWhitelistModel()
        global_model = GlobalWhitelistModel()

        client_matcher = WhitelistMatcher(client_model)
        global_matcher = WhitelistMatcher(global_model)

        url_matcher = UrlMatcher(client_matcher, global_matcher)

        match_broker = RabbitmqService(
            consume_queue=environ.get('VALIDATION_QUEUE'),
            post_exchange=environ.get('RESPONSE_EXCHANGE'),
            post_routing_key=environ.get('RESPONSE_ROUTING_KEY'),
            post_queue=environ.get('RESPONSE_QUEUE'))
        match_processor = MatchProcessor(match_broker, url_matcher)
        self.match_flow = Flow(match_processor)

        insert_broker = RabbitmqService(
            consume_queue=environ.get('INSERTION_QUEUE'))
        insert_processor = InsertProcessor(
            insert_broker, client_model, global_model)
        self.insert_flow = Flow(insert_processor)

    def _setUpDatabase(self):
        alembicArgs = [
            '--raiseerr',
            'upgrade', 'head',
        ]
        alembic.config.main(argv=alembicArgs)

    def _setUpDbSession(self):
        from models.connectors.mysqldb import MySQLDBConnection
        self.session = Session(MySQLDBConnection().connection)

    def _setUpBroker(self):
        self.rabbitmq_api = AdminAPI(url="http://%s:%s" % (environ.get('RABBITMQ_URL'), environ.get('RABBITMQ_API_PORT')),
                                     auth=(environ.get('RABBITMQ_USER'),
                                           environ.get('RABBITMQ_PASSWORD')))

        self.rabbitmq_api.create_vhost(environ.get('RABBITMQ_VHOST'))

    def setUp(self):

        load_dotenv(dotenv_path='tests/.env', override=True)
        self._setUpBroker()
        self._setUpDatabase()
        self._setUpDbSession()
        self._setUpApplication()

    def test_flow_insert_flow_client(self):
        payload = b'{"client": "pinterest", "regex": "^(https:\/\/)?(www.|m.)?pinterest\.com(.br)?(\/|\/\w+)?$"}'
        parsed_payload = RabbitmqCallback(
            self.insert_flow._flow_callback)._format_payload_to_dict(payload)

        self.insert_flow._flow_callback(parsed_payload)

        total_clients = self.session.query('* from client_whitelist').count()
        total_global = self.session.query('* from global_whitelist').count()

        self.assertEqual(total_clients, 1)
        self.assertEqual(total_global, 0)

    def test_flow_insert_flow_global(self):
        payload = b'{"client": "", "regex": "^(https:\/\/)?(www.|m.)?stackoverflow\.com(.br)?(\/|\/\w+)?$"}'
        parsed_payload = RabbitmqCallback(
            self.insert_flow._flow_callback)._format_payload_to_dict(payload)

        self.insert_flow._flow_callback(parsed_payload)

        total_clients = self.session.query('* from client_whitelist').count()
        total_global = self.session.query('* from global_whitelist').count()

        self.assertEqual(total_clients, 0)
        self.assertEqual(total_global, 1)

    def test_flow_match_flow_client_true(self):
        payload = b'{"client": "pinterest", "regex": "^(https:\/\/)?(www.|m.)?pinterest\.com(.br)?(\/|\/\w+)?$"}'
        parsed_payload = RabbitmqCallback(
            self.insert_flow._flow_callback)._format_payload_to_dict(payload)

        self.insert_flow._flow_callback(parsed_payload)

        payload = b'{"client": "pinterest","url": "www.pinterest.com", "correlationId": "' + \
            str(uuid4()).encode()+b'"}'
        parsed_payload = RabbitmqCallback(
            self.match_flow._flow_callback)._format_payload_to_dict(payload)

        result = self.match_flow._flow_callback(parsed_payload)

        self.assertIsInstance(result, dict)
        self.assertTrue(result['validation'])

    def test_flow_match_flow_client_false(self):
        payload = b'{"client": "linkedin", "regex": "^(https:\/\/)?(www.|m.)?linkedin\.com(.br)?(\/|\/\w+)?$"}'
        parsed_payload = RabbitmqCallback(
            self.insert_flow._flow_callback)._format_payload_to_dict(payload)

        self.insert_flow._flow_callback(parsed_payload)

        payload = b'{"client": "facebook","url": "www.facebook.com", "correlationId": "' + \
            str(uuid4()).encode()+b'"}'
        parsed_payload = RabbitmqCallback(
            self.match_flow._flow_callback)._format_payload_to_dict(payload)

        result = self.match_flow._flow_callback(parsed_payload)

        self.assertIsInstance(result, dict)
        self.assertFalse(result['validation'])

    def test_flow_match_flow_global_true(self):
        payload = b'{"client": "", "regex": "^(https:\/\/)?(www.|m.)?google\.com(.br)?(\/|\/\w+)?$"}'
        parsed_payload = RabbitmqCallback(
            self.insert_flow._flow_callback)._format_payload_to_dict(payload)

        self.insert_flow._flow_callback(parsed_payload)

        payload = b'{"client": "","url": "www.google.com", "correlationId": "' + \
            str(uuid4()).encode()+b'"}'
        parsed_payload = RabbitmqCallback(
            self.match_flow._flow_callback)._format_payload_to_dict(payload)

        result = self.match_flow._flow_callback(parsed_payload)

        self.assertIsInstance(result, dict)
        self.assertTrue(result['validation'])

    def test_flow_match_flow_global_false(self):
        payload = b'{"client": "", "regex": "^(https:\/\/)?(www.|m.)?linkedin\.com(.br)?(\/|\/\w+)?$"}'
        parsed_payload = RabbitmqCallback(
            self.insert_flow._flow_callback)._format_payload_to_dict(payload)

        self.insert_flow._flow_callback(parsed_payload)

        payload = b'{"client": "","url": "www.facebook.com", "correlationId": "' + \
            str(uuid4()).encode()+b'"}'
        parsed_payload = RabbitmqCallback(
            self.match_flow._flow_callback)._format_payload_to_dict(payload)

        result = self.match_flow._flow_callback(parsed_payload)

        self.assertIsInstance(result, dict)
        self.assertFalse(result['validation'])

    def _tearDownDatabase(self):
        self.session.close()
        alembicArgs = [
            '--raiseerr',
            'downgrade', 'base',
        ]
        alembic.config.main(argv=alembicArgs)

    def _tearDownBroker(self):
        self.rabbitmq_api.delete_vhost(environ.get('RABBITMQ_VHOST'))

    def tearDown(self):
        self._tearDownDatabase()
        self._tearDownBroker()


if __name__ == '__main__':
    unittest.main()
