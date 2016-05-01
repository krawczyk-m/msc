from netfilterqueue import NetfilterQueue
from scapy.layers.inet import IP
import pprint


def print_and_accept(pkt):
    ip = IP(pkt.get_payload())
    print "got packet from {}".format(ip[IP].src)
    #ip.show()
    #pkt.set_payload(str(ip))
    pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, print_and_accept)

try:
    nfqueue.run()
except KeyboardInterrupt:
    print
