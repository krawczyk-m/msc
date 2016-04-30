import unittest

from mock import MagicMock
from mock import Mock

from client.receiver.receiver import Receiver
from client.receiver.states import State
from client.messages.Messages import Messages


class ReceiverUnitTest(unittest.TestCase):

    def setUp(self):
        self.messenger = Mock()
        self.messenger.notify = MagicMock()

        self.transmitter = Mock()
        self.transmitter.send = MagicMock()

        self.receiver = Receiver(messenger=self.messenger, transmitter=self.transmitter)

    def test_after_create_idle(self):
        self.assertEqual(State.IDLE, self.receiver.state)

    def test_should_await_notify(self):
        self.receiver.await_notify()
        self.assertEqual(State.AWAIT_NOTIFY, self.receiver.state)

    def test_should_stay_in_await_notify(self):
        self.receiver.recvd_notify = MagicMock(return_value=False)

        self.receiver.await_notify()
        self.receiver.recv_notify()
        self.assertEqual(State.AWAIT_NOTIFY, self.receiver.state)
        self.receiver.recvd_notify.assert_called_once()

    def test_should_transition_to_listen_and_send_notify_ack(self):
        self.receiver.recvd_notify = MagicMock(return_value=True)

        self.receiver.await_notify()
        self.receiver.recv_notify()

        self.assertEqual(State.LISTEN, self.receiver.state)
        self.receiver.messenger.notify.assert_called_once_with(Messages.NOTIFY_ACK)

    def test_should_stay_in_listen(self):
        self.receiver.recvd_notify = MagicMock(return_value=True)
        self.receiver.recvd_steg = MagicMock(return_value=False)

        self.receiver.await_notify()
        self.receiver.recv_notify()
        self.receiver.recv_steganogram()

        self.assertEqual(State.LISTEN, self.receiver.state)
        self.receiver.recvd_steg.assert_called_once()

    def test_should_transition_to_await_report_ack_and_send_report(self):
        self.receiver.recvd_notify = MagicMock(return_value=True)
        self.receiver.recvd_steg = MagicMock(return_value=True)

        self.receiver.await_notify()
        self.receiver.recv_notify()
        self.receiver.recv_steganogram()

        self.assertEqual(State.AWAIT_REPORT_ACK, self.receiver.state)
        self.receiver.messenger.notify.assert_any_call(Messages.REPORT)

    def test_should_stay_in_await_report_ack(self):
        self.receiver.recvd_notify = MagicMock(return_value=True)
        self.receiver.recvd_steg = MagicMock(return_value=True)
        self.receiver.recvd_report_ack = MagicMock(return_value=False)

        self.receiver.await_notify()
        self.receiver.recv_notify()
        self.receiver.recv_steganogram()
        self.receiver.recv_report_ack()

        self.assertEqual(State.AWAIT_REPORT_ACK, self.receiver.state)
        self.receiver.recvd_report_ack.assert_called_once()

    def test_should_transition_to_fin(self):
        self.receiver.recvd_notify = MagicMock(return_value=True)
        self.receiver.recvd_steg = MagicMock(return_value=True)
        self.receiver.recvd_report_ack = MagicMock(return_value=True)

        self.receiver.await_notify()
        self.receiver.recv_notify()
        self.receiver.recv_steganogram()
        self.receiver.recv_report_ack()

        self.assertEqual(State.FIN, self.receiver.state)
