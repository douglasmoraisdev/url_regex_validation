from utils import regex_utils
from utils.log_utils import log

class InsertProcessor:

    def __init__(self, broker, client_model, global_model):
        self.broker = broker
        self.client_model = client_model
        self.global_model = global_model
        self.log = log

    def _is_client_regex(self, payload: dict):

        try:
            return (payload['client'] is not None) and (not payload['client'].strip() == "")

        except Exception as e:
            self.log.error(f"Error on process payload {e}")

    def _is_valid_payload(self, payload):

        is_valid_regex = False

        required_fields = ['client',
                           'regex']

        is_required_fields = len(set(required_fields) & set(
            payload.keys())) == len(required_fields)

        if is_required_fields:
            is_valid_regex = regex_utils.is_valid_regex(payload['regex'])

        return is_required_fields and is_valid_regex

    def process(self, payload: dict):

        if self._is_valid_payload(payload):

            if self._is_client_regex(payload):

                client_name = payload['client']
                regex = payload['regex']

                response = self.client_model.insert_client_regex(client_name, regex)

                self.log.info(f"Added new regex [client]: {payload}")

                return payload

            else:

                regex = payload['regex']

                response = self.global_model.insert_global_regex(regex)

                self.log.info(f"Added new regex [global]: {payload}")

                return payload

        else:
            self.log.error('Invalid payload %s' % str(payload))
