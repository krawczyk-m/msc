
import time

from transitions import Machine
from states import State


class Sender(object):

    notifier = None

    states = [
        State.IDLE,
        State.NOTIFY_SENT,
        State.AWAIT_REPORT,
        State.FIN
    ]

    state_methods = None

    def __init__(self, notifier, receiver, messenger):
        self.notifier = notifier
        self.receiver = receiver
        self.messenger = messenger

        self.triggers = {
            State.IDLE: "send_notify",
            State.NOTIFY_SENT: "recv_notify_ack",
            State.AWAIT_REPORT: "recv_report",
        }

        self.machine = Machine(model=self, states=Sender.states, initial=State.IDLE)

        self.machine.add_transition(trigger="send_notify", source=State.IDLE, dest=State.NOTIFY_SENT)
        self.machine.on_exit_idle("notify")

        self.machine.add_transition(trigger="recv_notify_ack", source=State.NOTIFY_SENT, dest=State.AWAIT_REPORT,
                                    conditions=["recvd_notify_ack"])
        self.machine.on_exit_notify_sent("send_message")

        self.machine.add_transition(trigger="recv_message_ack", source=State.AWAIT_REPORT, dest=State.FIN,
                                    conditions=["recvd_message_ack"])
        self.machine.on_exit_await_report("confirm")

    def run(self):
        while self.state != State.FIN:
            trigger = self.triggers[self.state]
            getattr(self, trigger)()
            time.sleep(1)

    def notify(self):
        print "Notifying"
        self.notifier.notify()

    def recvd_notify_ack(self):
        return self.receiver.receive()

    def send_message(self):
        print "Sending message"
        self.messenger.send()

    def recvd_message_ack(self):
        print "Recv message ack"
        pass

    def confirm(self):
        self.notifier.notify()


