import ast
from utils import url_utils
from utils.log_utils import log


class MatchProcessor:

    def __init__(self, broker, url_matcher):
        self.url_matcher = url_matcher
        self.broker = broker
        self.log = log

    def _is_valid_payload(self, payload):

        is_valid_correlationId = False
        is_valid_url = False

        required_fields = ['url',
                           'client',
                           'correlationId']

        is_required_fields = len(set(required_fields) & set(
            payload.keys())) == len(required_fields)

        if is_required_fields:
            is_valid_correlationId = len(payload['correlationId'].strip()) > 0
            is_valid_url = url_utils.is_valid_url(payload['url'])

        return is_required_fields and is_valid_correlationId and is_valid_url

    def _format_validation_output(self, validation_result, correlationId):

        if validation_result:
            response = u"{'regex': '%s', 'validation': True, 'correlationId': '%s'}" % (
                validation_result, correlationId)

        else:
            response = u"{'regex': 'null', 'validation': False, 'correlationId': '%s'}" % correlationId

        return response

    def process(self, payload: dict):

        if self._is_valid_payload(payload):

            url = payload['url']
            client = payload['client'].strip()
            correlationId = payload['correlationId']

            validation_result = self.url_matcher.match_url(url, client)

            broker_payload = self._format_validation_output(
                validation_result, correlationId)

            self.broker.post(broker_payload)

            return ast.literal_eval(broker_payload)

        else:
            self.log.error('Invalid payload %s' % str(payload))

