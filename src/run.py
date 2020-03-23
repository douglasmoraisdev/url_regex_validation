#!/usr/bin/env python3
from app import App

from services.rabbitmq import RabbitmqService

from core.url_matcher import UrlMatcher
from core.whitelist_matcher import WhitelistMatcher
from core.match_processor import MatchProcessor
from core.insert_processor import InsertProcessor

from core.flow import Flow

from models.client_whitelist import ClientWhitelistModel
from models.global_whitelist import GlobalWhitelistModel

from os import environ
from dotenv import load_dotenv

load_dotenv()

client_model = ClientWhitelistModel()
global_model = GlobalWhitelistModel()

client_matcher = WhitelistMatcher(client_model)
global_matcher = WhitelistMatcher(global_model)

url_matcher = UrlMatcher(client_matcher, global_matcher)

match_broker = RabbitmqService(
    consume_queue=environ.get('VALIDATION_QUEUE'),
    post_exchange=environ.get('RESPONSE_EXCHANGE'),
    post_routing_key=environ.get('RESPONSE_ROUTING_KEY'),
    post_queue=environ.get('RESPONSE_QUEUE')
    )
match_processor = MatchProcessor(match_broker, url_matcher)
match_flow = Flow(match_processor)

insert_broker = RabbitmqService(consume_queue=environ.get('INSERTION_QUEUE'))
insert_processor = InsertProcessor(insert_broker, client_model, global_model)
insert_flow = Flow(insert_processor)

app = App()
app.run(match_flow, insert_flow)