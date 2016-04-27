import unittest
import pika

from client.messengers.RabbitMQClient import RabbitMQClient


class RabbitMQClientIntegrationTest(unittest.TestCase):
    """
    Requires RabbitMQ server to be listening @localhost:5672 with guest:guest user/password
    """
    def setUp(self):
        self.config = {
            "host": "localhost",
            "listen_queue": "queue",
            "notify_queue": "queue",
        }

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.config["host"]))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.config["listen_queue"])

        self.client = RabbitMQClient(self.config)

    def tearDown(self):
        self.channel.queue_delete(queue=self.config["listen_queue"])
        self.connection.close()
        self.client.join()  # empty

    def test_message_round_trip(self):
        self.client.notify("test_message")
        rt_message = self.client.receive()
        self.assertEqual("test_message", rt_message)

        self.client.notify("another_message")
        rt_message = self.client.receive()
        self.assertEqual("another_message", rt_message)
