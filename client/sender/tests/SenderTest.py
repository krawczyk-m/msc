import unittest

from mock import MagicMock
from mock import Mock
from client.sender.sender import Sender
from client.sender.states import State


class SenderTest(unittest.TestCase):

    def setUp(self):
        self.notifier = Mock()
        self.notifier.notify = MagicMock()

        self.receiver = Mock()
        self.receiver.receive = MagicMock()

        self.messenger = Mock()
        self.messenger.send = MagicMock()

        self.sender = Sender(notifier=self.notifier, receiver=self.receiver, messenger=self.messenger)

    def test_after_create_idle(self):
        self.assertEqual(State.IDLE, self.sender.state)

    def test_should_notify_and_transition(self):
        self.sender.send_notify()
        self.sender.notifier.notify.assert_called_once()
        self.assertEqual(State.NOTIFY_SENT, self.sender.state)

    def test_should_stay_in_notify_sent(self):
        self.sender.recvd_notify_ack = MagicMock(return_value=False)

        self.sender.send_notify()
        self.sender.recv_notify_ack()
        self.assertEqual(State.NOTIFY_SENT, self.sender.state)

    def test_should_send_message_and_transition_to_await_report(self):
        self.sender.recvd_notify_ack = MagicMock(return_value=True)

        self.sender.send_notify()
        self.sender.recv_notify_ack()

        self.assertEqual(State.AWAIT_REPORT, self.sender.state)
        self.sender.messenger.send.assert_called_once()

    def test_should_stay_in_await_report(self):
        self.sender.recvd_notify_ack = MagicMock(return_value=True)
        self.sender.recvd_message_ack = MagicMock(return_value=False)

        self.sender.send_notify()
        self.sender.recv_notify_ack()
        self.sender.recv_message_ack()
        self.assertEqual(State.AWAIT_REPORT, self.sender.state)

    def test_should_send_confirmation_and_transition(self):
        self.sender.recvd_notify_ack = MagicMock(return_value=True)
        self.sender.recvd_message_ack = MagicMock(return_value=True)

        self.sender.send_notify()
        self.sender.recv_notify_ack()
        self.sender.recv_message_ack()
        self.assertEqual(2, len(self.sender.notifier.mock_calls))
        self.assertEqual(State.FIN, self.sender.state)