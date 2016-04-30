from transitions import Machine
from states import State
from client.messages.Messages import Messages


class Sender(object):
    """
    Class representing the endpoint of the steganographic communication initiating
    the steganographic connection setup.
    """
    config = None
    messenger = None
    transmitter = None
    steganogram = None

    states = [
        State.IDLE,
        State.NOTIFY_SENT,
        State.LISTEN,
        State.AWAIT_REPORT,
        State.FIN
    ]

    def __init__(self, config, messenger, transmitter):
        """
        :param config:          configuration parameters for the sender
        :param messenger:       object responsible for communicating the desire of setting up a covert channel
                                should have:
                                notify() - notifies the other endpoint that is about to start sending stegano packets
                                receive() - listens for and receives confirmations of notify()
        :param transmitter:     object responsible for handling the steganographic communication
        """
        self.config = config
        self.messenger = messenger
        self.transmitter = transmitter

        self.steganogram = self.config.get("Steg", "steganogram")

        self.triggers = {
            State.IDLE: "send_notify",
            State.NOTIFY_SENT: "recv_notify_ack",
            State.LISTEN: "recv_pkt",
            State.AWAIT_REPORT: "recv_report",
        }

        self.machine = Machine(model=self, states=Sender.states, initial=State.IDLE)

        self.machine.add_transition(trigger=self.triggers[State.IDLE], source=State.IDLE, dest=State.NOTIFY_SENT)
        self.machine.on_exit_idle("notify")

        self.machine.add_transition(trigger=self.triggers[State.NOTIFY_SENT], source=State.NOTIFY_SENT, dest=State.LISTEN,
                                    conditions=["recvd_notify_ack"])
        # TODO: self.machine.on_exit_notify_sent("configure_iptables")

        self.machine.add_transition(trigger=self.triggers[State.LISTEN], source=State.LISTEN, dest=State.AWAIT_REPORT,
                                    conditions=["sent_steg"])

        self.machine.add_transition(trigger=self.triggers[State.AWAIT_REPORT], source=State.AWAIT_REPORT, dest=State.FIN,
                                    conditions=["recvd_report"])
        self.machine.on_exit_await_report("send_report_ack")

    def run(self):
        while self.state != State.FIN:
            trigger = self.triggers[self.state]
            getattr(self, trigger)()

    def notify(self):
        print "Notifying"
        self.messenger.notify(Messages.NOTIFY)

    def recvd_notify_ack(self):
        return self.messenger.receive()

    def sent_steg(self):
        return self.steganogram is None

    def recvd_report(self):
        return self.messenger.receive()

    def send_report_ack(self):
        print "Sending report ack"
        self.messenger.notify(Messages.REPORT_ACK)


