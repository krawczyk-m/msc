from netfilterqueue import NetfilterQueue
from scapy.layers.inet import IP

import threading
import time

from transitions import Machine
from states import State
from client.messages.Messages import Messages


class Receiver(object):
    """
    Class representing the endpoint of the steganographic communication waiting for
    the steganographic connection setup initiation.
    """
    messenger = None
    transmitter = None
    steganogram = []

    listening_thread = None

    states = [
        State.IDLE,
        State.AWAIT_NOTIFY,
        State.LISTEN,
        State.AWAIT_REPORT_ACK,
        State.FIN
    ]

    def __init__(self, config, messenger, transmitter):
        """self._handle_outgoing_packets
        :param messenger:       object responsible for listening for steganographic connection initiation notificaiton
                                from another endpoint
                                should have:
                                receive() - listens for and responds to notify messages
                                notify() - for sending acknowledgements
        :param transmitter:     object responsible for handling the steganographic communication - sending/receiving bits
        """
        self.config = config
        self.messenger = messenger
        self.transmitter = transmitter

        self._load_config()

        self.triggers = {
            State.IDLE: "await_notify",
            State.AWAIT_NOTIFY: "recv_notify",
            State.LISTEN: "recv_steganogram",
            State.AWAIT_REPORT_ACK: "recv_report_ack"
        }

        self.machine = Machine(model=self, states=Receiver.states, initial=State.IDLE)

        self.machine.add_transition(trigger=self.triggers[State.IDLE], source=State.IDLE, dest=State.AWAIT_NOTIFY)

        self.machine.add_transition(trigger=self.triggers[State.AWAIT_NOTIFY], source=State.AWAIT_NOTIFY, dest=State.LISTEN,
                                    conditions=["recvd_notify"])
        self.machine.on_exit_await_notify("send_notify_ack")

        self.machine.add_transition(trigger=self.triggers[State.LISTEN], source=State.LISTEN, dest=State.AWAIT_REPORT_ACK,
                                    conditions=["recvd_steg"])
        self.machine.on_exit_listen("send_report")

        self.machine.add_transition(trigger=self.triggers[State.AWAIT_REPORT_ACK], source=State.AWAIT_REPORT_ACK,
                                    dest=State.FIN, conditions=["recvd_report_ack"])

    def run(self):
        self.listening_thread = threading.Thread(name="ListenThread", target=self._nfqueue_receive)
        self.listening_thread.start()

        while self.state != State.LISTEN:
            print self.receiver.state
            trigger = self.triggers[self.state]
            getattr(self, trigger)()

    def recvd_notify(self):
        message = self.messenger.receive()
        return message == Messages.NOTIFY

    def send_notify_ack(self):
        print "Received notify. Sending ACK"
        self.messenger.notify(Messages.NOTIFY_ACK)

    def recvd_steg(self):
        return self.steganogram is not None

    # TODO report needs two values - positive and negative
    # TODO compare if received steganogram is as expected
    def send_report(self):
        print "Received steganogram: {}. Sending report".format(reduce(lambda x, y: x + y, self.steganogram, ""))
        self.messenger.notify(Messages.REPORT)

    def recvd_report_ack(self):
        message = self.messenger.receive()
        return message == Messages.REPORT_ACK

    def _nfqueue_receive(self):
        self.nfqueue = NetfilterQueue()
        self.nfqueue.bind(self.listen_queue_num, self._handle_incoming_packets)

    def _handle_incoming_packets(self, pkt):
        if self.state is State.LISTEN:
            ip_packet = IP(pkt)
            self.steganogram = self.transmitter.extract(ip_packet)
        pkt.accept()

    def _load_config(self):
        self.expected_steganogram = self.config.get("Steg", "steganogram")
        self.listen_queue_num = self.config.get("NFQueue", "listen_queue_num")


