from protocols.IPProtocol import IPProtocol
from protocols.util.BitConverter import BitConverter
from protocols.error.LayerNotFound import LayerNotFoundError


class IPIdentification(IPProtocol):
    """
    Modifies the Identification field of the IP protocol
    """
    field = "id"
    max_bits = 16

    @classmethod
    def set(cls, packet, bit_array):
        if len(bit_array) > cls.max_bits:
            raise ValueError("You can not set more bits than {}".format(cls.max_bits))
        setattr(packet, cls.field, BitConverter.int(bit_array))
        return packet

    # TODO use bits limiting
    @classmethod
    def get(cls, packet, bits=0):
        layer = packet.getlayer(cls.layer)
        if not layer:
            raise LayerNotFoundError("Layer {} not found in packet".format(cls.layer))
        return getattr(layer, cls.field)


