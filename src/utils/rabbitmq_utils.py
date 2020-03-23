import ast
from utils.log_utils import log

class RabbitmqCallback:

    def __init__(self, callback_target):
        self.callback_target = callback_target
        self.log = log

    def _format_payload_to_dict(self, payload_body):

        dict_body = ast.literal_eval(payload_body.decode('utf-8'))
        return dict_body

    def callback_dict_body(self, ch, method, properties, body):

        dict_body = {}

        try:
            dict_body = self._format_payload_to_dict(body)
        except SyntaxError as sintax_error:
            self.log.error('Invalid payload format %s' % str(body))
        except Exception as exception:
            self.log.error(f"Exception on payload format. Error: {exception} - Payload {body}")

        if dict_body:
            self.callback_target(dict_body)
