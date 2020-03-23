import pika
from os import environ
from dotenv import load_dotenv
from utils.log_utils import log

load_dotenv()

class RabbitmqService:

    def __init__(self, consume_queue='', post_routing_key='', post_exchange='', post_queue=''):
        self.consume_queue = consume_queue
        self.post_routing_key = post_routing_key
        self.post_exchange = post_exchange
        self.post_queue = post_queue
        self.log = log

        self._create_connection()

        if consume_queue:
            self.channel.queue_declare(queue=consume_queue)

        if post_queue:
            self.channel.queue_declare(queue=post_queue)

        if post_exchange:
            self.channel.queue_declare(queue=post_queue)
            self.channel.exchange_declare(exchange=post_exchange)
            self.channel.queue_bind(post_queue, post_exchange, post_routing_key)

    def _create_connection(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(environ.get('RABBITMQ_URL'), 
                                      environ.get('RABBITMQ_PORT'), 
                                      virtual_host=environ.get('RABBITMQ_VHOST')))
        self.channel = self.connection.channel()


    def consume(self, callback):

        while True:
            try:
                self.channel.basic_qos(prefetch_count=1)
                self.channel.basic_consume(queue=self.consume_queue,
                                        on_message_callback=callback,
                                        auto_ack=True
                                        )

                return self.channel.start_consuming()

            except pika.exceptions.ConnectionClosedByBroker:
                break

            except pika.exceptions.AMQPChannelError:
                break

            except pika.exceptions.AMQPConnectionError:
                continue

    def post(self, message):
        self.channel.basic_publish(exchange=self.post_exchange,
                                   routing_key=self.post_routing_key,
                                   body=message)

        self.log.info("Sent validation response [%s]" % message)

    def close_connection(self):

        self.connection.close()
