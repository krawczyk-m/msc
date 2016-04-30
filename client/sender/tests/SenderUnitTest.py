import unittest
import ConfigParser

from mock import MagicMock
from mock import Mock

from client.sender.sender import Sender
from client.sender.states import State
from client.messages.Messages import Messages


class SenderUnitTest(unittest.TestCase):

    def setUp(self):
        self.messenger = Mock()
        self.messenger.notify = MagicMock()

        self.transmitter = Mock()
        self.transmitter.send = MagicMock()

        self.config = ConfigParser.ConfigParser()
        self.config.read('config.conf')

        self.sender = Sender(config=self.config, messenger=self.messenger, transmitter=self.transmitter)

    def test_after_create_idle(self):
        self.assertEqual(State.IDLE, self.sender.state)

    def test_should_notify_and_transition(self):
        self.sender.send_notify()

        self.sender.messenger.notify.assert_called_once_with(Messages.NOTIFY)
        self.assertEqual(State.NOTIFY_SENT, self.sender.state)

    def test_should_stay_in_notify_sent(self):
        self.sender.recvd_notify_ack = MagicMock(return_value=False)

        self.sender.send_notify()
        self.sender.recv_notify_ack()
        self.assertEqual(State.NOTIFY_SENT, self.sender.state)

    def test_should_transition_to_listen(self):
        self.sender.recvd_notify_ack = MagicMock(return_value=True)

        self.sender.send_notify()
        self.sender.recv_notify_ack()

        self.assertEqual(State.LISTEN, self.sender.state)

    def test_should_stay_in_listen(self):
        self.sender.recvd_notify_ack = MagicMock(return_value=True)
        self.sender.sent_steg = MagicMock(return_value=False)

        self.sender.send_notify()
        self.sender.recv_notify_ack()
        self.sender.recv_pkt()

        self.assertEqual(State.LISTEN, self.sender.state)

    def test_should_transition_to_await_report(self):
        self.sender.recvd_notify_ack = MagicMock(return_value=True)
        self.sender.sent_steg = MagicMock(return_value=True)

        self.sender.send_notify()
        self.sender.recv_notify_ack()
        self.sender.recv_pkt()

        self.assertEqual(State.AWAIT_REPORT, self.sender.state)

    def test_should_stay_in_await_report(self):
        self.sender.recvd_notify_ack = MagicMock(return_value=True)
        self.sender.sent_steg = MagicMock(return_value=True)
        self.sender.recvd_report = MagicMock(return_value=False)

        self.sender.send_notify()
        self.sender.recv_notify_ack()
        self.sender.recv_pkt()
        self.sender.recv_report()
        self.assertEqual(State.AWAIT_REPORT, self.sender.state)

    def test_should_send_report_ack_and_transition_to_fin(self):
        self.sender.recvd_notify_ack = MagicMock(return_value=True)
        self.sender.sent_steg = MagicMock(return_value=True)
        self.sender.recvd_report = MagicMock(return_value=True)

        self.sender.send_notify()
        self.sender.recv_notify_ack()
        self.sender.recv_pkt()
        self.sender.recv_report()

        self.assertEqual(State.FIN, self.sender.state)
        self.sender.messenger.notify.assert_any_call(Messages.REPORT_ACK)