import unittest
import pika
from ConfigParser import ConfigParser

from client.messengers.RabbitMQClient import RabbitMQClient


class RabbitMQClientIntegrationTest(unittest.TestCase):
    """
    Requires RabbitMQ server to be listening @host:5672 with guest:guest user/password
    """
    def setUp(self):
        self.config = ConfigParser()
        self.config.read('config.conf')

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.config.get("RabbitMQ", "host")))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.config.get("RabbitMQ", "inbound_queue"))

        self.client = RabbitMQClient(self.config)

    def tearDown(self):
        self.channel.queue_delete(queue=self.config.get("RabbitMQ", "inbound_queue"))
        self.connection.close()
        self.client.join()  # empty

    def test_message_round_trip(self):
        self.client.notify("test_message")
        rt_message = self.client.receive()
        self.assertEqual("test_message", rt_message)

        self.client.notify("another_message")
        rt_message = self.client.receive()
        self.assertEqual("another_message", rt_message)
