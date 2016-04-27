import pika
import threading


class RabbitMQClient(object):
    def __init__(self, config):
        self.response = None
        self.config = config

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.config["host"]))
        self.channel = self.connection.channel()

        self.channel.basic_consume(self._receive, no_ack=True, queue=self.config["listen_queue"])
        self.consume_thread = threading.Thread(target=self._consume)
        self.consume_thread.start()

    def _consume(self):
        self.channel.start_consuming()

    def _receive(self, ch, method, properties, body):
        self.response = body

    def receive(self):
        self.response = None
        while self.response is None:
            self.connection.process_data_events()
        return self.response

    def notify(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.config["notify_queue"],
                                   body=message)

    def join(self):
        # self.channel.stop_consuming() # seems to not break channel.start_consuming()
        # self.consume_thread.join() # since channel.start_consuming() does not stop, this hangs forever
        pass