from netfilterqueue import NetfilterQueue
from scapy.layers.inet import IP

import ConfigParser
import threading
import time

from transitions import Machine
from states import State
from client.messages.Messages import Messages

from client.messengers.RabbitMQClient import RabbitMQClient
from client.transmitter import Transmitter
from protocols.IPIdentification import IPIdentification


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

        while self.state != State.FIN:
            print str(self.state)
            trigger = self.triggers[self.state]
            getattr(self, trigger)()
            time.sleep(2)  # for presentation purposes on seminar

    def recvd_notify(self):
        message = self.messenger.receive()
        print "Received message: {}".format(message)
        return message == Messages.NOTIFY

    def send_notify_ack(self):
        print "Sending {}".format(Messages.NOTIFY_ACK)
        self.messenger.notify(Messages.NOTIFY_ACK)

    def recvd_steg(self):
        return len(self.steganogram) != 0

    # TODO report needs two values - positive and negative
    # TODO compare if received steganogram is as expected
    def send_report(self):
        print "Received steganogram: {}. Sending {}".format(reduce(lambda x, y: str(x) + str(y), self.steganogram, ""),
                                                            Messages.REPORT)
        self.messenger.notify(Messages.REPORT)

    def recvd_report_ack(self):
        message = self.messenger.receive()
        if message == Messages.REPORT_ACK:
            print "Received {}. Ending conversation".format(Messages.REPORT_ACK)
            return True
        return False

    def _nfqueue_receive(self):
        self.nfqueue = NetfilterQueue()
        self.nfqueue.bind(self.listen_queue_num, self._handle_incoming_packets)
        self.nfqueue.run()

    def _handle_incoming_packets(self, pkt):
        ip_packet = IP(pkt.get_payload())
        print "Handling incoming packet."
        if self.state is State.LISTEN:
            self.steganogram = self.transmitter.extract(ip_packet)
        pkt.accept()

    def _load_config(self):
        self.expected_steganogram = self.config.get("Steg", "steganogram")
        self.listen_queue_num = int(self.config.get("NFQueue", "listen_queue_num"))

if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read('config.conf')

    messenger = RabbitMQClient(config)
    transmitter = Transmitter(protocols=[IPIdentification])

    receiver = Receiver(config, messenger, transmitter)

    try:
        receiver.run()
    except KeyboardInterrupt:
        print "Interrupted"
