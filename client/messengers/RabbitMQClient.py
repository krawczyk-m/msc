import pika
import threading


class RabbitMQClient(object):
    def __init__(self, config):
        self.response = None
        self.config = config

        self._load_config()

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.rabbit_host))
        self.channel = self.connection.channel()

    def receive(self):
        self.response = None
        while self.response is None:
            self.response = self.channel.basic_get(queue=self.inbound_queue, no_ack=True)[2]
        return self.response

    def notify(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.outbound_queue,
                                   body=message)

    def join(self):
        # self.channel.stop_consuming() # seems to not break channel.start_consuming()
        # self.consume_thread.join() # since channel.start_consuming() does not stop, this hangs forever
        pass

    # TODO try to do this with RPC queues...
    def _load_config(self):
        self.rabbit_host = self.config.get("RabbitMQ", "host")
        self.outbound_queue = self.config.get("RabbitMQ", "outbound_queue")
        self.inbound_queue = self.config.get("RabbitMQ", "inbound_queue")
