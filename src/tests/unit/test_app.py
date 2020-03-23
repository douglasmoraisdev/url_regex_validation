#!/usr/bin/env python3
import unittest
from unittest.mock import MagicMock
from app import App
from services.rabbitmq import RabbitmqService
from core.url_matcher import UrlMatcher
from core.match_processor import MatchProcessor
from core.insert_processor import InsertProcessor
from core.flow import Flow

class TestApp(unittest.TestCase):

    def test_app_run_all_flows(self):

        mock_flow_processor = MagicMock(return_value=True)
        flow_1 = Flow(mock_flow_processor)
        flow_2 = Flow(mock_flow_processor)
        flow_3 = Flow(mock_flow_processor)

        app = App()

        runs = app.run(flow_1, flow_2, flow_3)

        self.assertIsInstance(runs, list)
        self.assertEqual(len(runs), 3)

    def test_app_run_finish_status(self):

        mock_flow_processor = MagicMock(return_value=True)
        flow = Flow(mock_flow_processor)

        app = App()

        runs = app.run(flow)

        self.assertIsInstance(runs, list)
        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0]._state, 'FINISHED')

if __name__ == '__main__':
    unittest.main()
