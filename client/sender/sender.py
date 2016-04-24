
import time

from transitions import Machine
from states import State


class Sender(object):

    notifier = None

    states = [
        State.INIT,
        State.NOTIFY,
        State.AWAIT_CONFIRMATION,
        State.SEND,
        State.AWAIT_REPORT,
        State.CONFIRM_REPORT
    ]

    def __init__(self, notifier):
        self.notifier = notifier

        self.machine = Machine(model=self, states=Sender.states, initial=State.INIT)

        self.machine.add_transition(trigger="run", source=State.INIT, dest=State.NOTIFY)
        self.machine.on_exit_init('exit_init')

        self.machine.on_enter_notify("enter_notify")
        self.machine.add_transition(trigger="notify", source=State.NOTIFY, dest=State.AWAIT_CONFIRMATION)

        self.machine.on_enter_await_confirmation("enter_await_confirmation")

    def exit_init(self):
        print "Initialised sender"
        # time.sleep(1)

    def enter_notify(self):
        print "Notifying"
        self.notifier.notify()
        self.notify()

    def enter_await_confirmation(self):
        pass



