from utils.rabbitmq_utils import RabbitmqCallback

class Flow:

    def __init__(self, processor):
        self.processor = processor

    def _flow_callback(self, payload: dict):
        return self.processor.process(payload)

    def run(self):

        callback_parse = RabbitmqCallback(self._flow_callback)

        self.processor.broker.consume(callback=callback_parse.callback_dict_body)
