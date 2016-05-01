import nfqueue, socket
from scapy.layers.inet import IP
import pprint


def print_and_accept(*args):
    for i in args:
        if isinstance(i, nfqueue.payload):
            payload = i
    ip = IP(payload.get_data())
    print "got packet to {}".format(ip[IP].dst)
    ip[IP].id = 49152

    payload.set_verdict_modified(nfqueue.NF_ACCEPT, str(ip), len(ip))

q = nfqueue.queue()
q.set_callback(print_and_accept)
q.open()
q.create_queue(1)
try:
    q.try_run()
except KeyboardInterrupt, e:
    print "interruption"

q.unbind(socket.AF_INET)
q.close()
