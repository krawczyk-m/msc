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


class Sender(object):
    """
    Class representing the endpoint of the steganographic communication initiating
    the steganographic connection setup.
    """
    config = None
    messenger = None
    transmitter = None
    steganogram = None

    sending_thread = None

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

        self._load_config()

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
        self.sending_thread = threading.Thread(name="SendThread", target=self._nfqueue_send)
        self.sending_thread.start()

        while self.state != State.FIN:
            print str(self.state)
            trigger = self.triggers[self.state]
            getattr(self, trigger)()
            time.sleep(2)  # for presentation purposes on seminar

    def notify(self):
        print "Sending {}".format(Messages.NOTIFY)
        self.messenger.notify(Messages.NOTIFY)

    def recvd_notify_ack(self):
        if self.messenger.receive() == Messages.NOTIFY_ACK:
            print "Received {}. Will embed steganogram in next packet".format(Messages.NOTIFY_ACK)
            return True
        return False

    def sent_steg(self):
        if self.steganogram is None:
            print "Steganogram embedded. Waiting for {}".format(Messages.REPORT)
            return True
        return False

    def recvd_report(self):
        if self.messenger.receive() == Messages.REPORT:
            print "Received {}".format(Messages.REPORT)
            return True
        return False

    def send_report_ack(self):
        print "Sending {}. Ending conversation".format(Messages.REPORT_ACK)
        self.messenger.notify(Messages.REPORT_ACK)

    def _nfqueue_send(self):
        self.nfqueue = NetfilterQueue()
        self.nfqueue.bind(self.send_queue_num, self._handle_outgoing_packets)
        self.nfqueue.run()

    def _handle_outgoing_packets(self, pkt):
        print "Handling outgoing packet."
        if self.state is State.LISTEN:
            ip_packet = IP(pkt.get_payload())
            ip_packet = self.transmitter.embed(ip_packet, self.steganogram)
            self.steganogram = None
            pkt.set_payload(str(ip_packet))
        pkt.accept()

    def _load_config(self):
        string_steg = self.config.get("Steg", "steganogram")
        self.steganogram = [int(x) for x in string_steg]
        self.send_queue_num = int(self.config.get("NFQueue", "send_queue_num"))

if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read('config.conf')

    messenger = RabbitMQClient(config)
    transmitter = Transmitter(protocols=[IPIdentification])

    sender = Sender(config, messenger, transmitter)

    try:
        sender.run()
    except KeyboardInterrupt:
        print "Interrupted"
