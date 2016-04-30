
class Transmitter(object):
    """
    Class providing the actual steganographic logic of embedding hidden data in network packets
    based on the list of configured, used protocols
    Provides the embedding and extraction methods
    """
    protocols = []

    def __init__(self, protocols=[]):
        """
        Initializes the transmitter with a set of protocols to use in the steganographic communication
        :param protocols:       set of protocols to use for steganographic communication
        """
        self.protocols = protocols

    # TODO 1 functionality between protocols may collide?
    # TODO 2 what if len(bit_array) greater than available bit space for all protocols?
    # TODO 3 same as 2 for a single protocol - need better handling e.g. return the bits that are left
    def embed(self, packet, bit_array):
        """
        Embeds the bit_array into the passed in packet
        :param packet:      scapy.layers.inet.IP packet
        :param bit_array:   bit array in the form of integer 0's and 1's
        :return:            modified scapy.layers.inet.IP packet with steganographic bits
        """
        for protocol in self.protocols:
            packet = protocol.set(packet, bit_array)
        return packet

    def extract(self, packet):
        """
        Extracts steganographic bits from the passed in packet
        :param packet:       scapy.layers.inet.IP packet
        :return:             bit array in the form of integer 0's and 1's
        """
        bit_array = []
        for protocol in self.protocols:
            bit_array.extend(protocol.get(packet))
        return bit_array
