import unittest

from mock import MagicMock
from mock import Mock
from client.sender.sender import Sender
from client.sender.states import State


class SenderTest(unittest.TestCase):

    def setUp(self):
        self.notifier = Mock()
        self.sender = Sender(notifier=self.notifier)

    def test_after_create_init(self):
        self.assertEqual(State.INIT, self.sender.state)

    def test_should_notify_on_enter(self):
        self.sender.enter_notify = MagicMock()
        self.sender.run()
        self.sender.enter_notify.assert_called_once_with()

    def test_should_transition_to_notify(self):
        self.sender.enter_notify = MagicMock()
        self.sender.run()
        self.assertEqual(State.NOTIFY, self.sender.state)

    def test_should_transition_to_await_confirmation(self):
        self.sender.run()
        self.assertEqual(State.AWAIT_CONFIRMATION, self.sender.state)





