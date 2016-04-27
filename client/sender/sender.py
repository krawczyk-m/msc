
import time

from transitions import Machine
from states import State


class Sender(object):
    """
    Class representing the endpoint of the steganographic communication initiating
    the steganographic connection setup.
    """
    messenger = None
    transmitter = None

    states = [
        State.IDLE,
        State.NOTIFY_SENT,
        State.AWAIT_REPORT,
        State.FIN
    ]

    def __init__(self, messenger, transmitter):
        """

        :param messenger:       object responsible for communicating the desire of setting up a covert channel
                                should have:
                                notify() - notifies the other endpoint that is about to start sending stegano packets
                                receive() - listens for and receives confirmations of notify()
        :param transmitter:     object responsible for handling the steganographic communication
        :return:
        """
        self.messenger = messenger
        self.transmitter = transmitter

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

    def notify(self):
        print "Notifying"
        self.messenger.notify()

    def recvd_notify_ack(self):
        return self.messenger.receive()

    def send_message(self):
        print "Sending message"
        self.transmitter.send()

    def recvd_message_ack(self):
        return self.messenger.receive()

    def confirm(self):
        self.messenger.notify()


