from protocols.IPProtocol import IPProtocol
from protocols.util.BitConverter import BitConverter
from protocols.error.LayerNotFoundError import LayerNotFoundError
from scapy.layers.inet import IP

class IPIdentification(IPProtocol):
    """
    Modifies the Identification field of the IP protocol
    """
    field = "id"
    max_bits = 16

    @classmethod
    def set(cls, packet, bit_array):
        if not isinstance(bit_array, list):
            return packet
        if len(bit_array) > cls.max_bits:
            raise ValueError("You can not set more bits than {}".format(cls.max_bits))
        value = BitConverter.int(bit_array)
        print "Setting IP id value from: {} to {}".format(packet[IP].id, value)
        setattr(packet, cls.field, value)
        return packet

    # TODO use bits limiting - it might be so that we use less bits than are available in the protocol e.g. only 4 bits for IPIdentification
    @classmethod
    def get(cls, packet, bits=0):
        layer = packet.getlayer(cls.layer)
        if not layer:
            raise LayerNotFoundError("Layer {} not found in packet".format(cls.layer))
        return BitConverter.bit_array(getattr(layer, cls.field))


