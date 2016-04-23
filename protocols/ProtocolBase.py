

class ProtocolBase(object):
    """This is a base class representing a family of possible protocols
    which can be used for steganography communication

    Attributes:
        layer       The name of the layer the protocol operates in
        field       The name of the field the protocol operates on
    """
    layer = ""
    field = ""

    @staticmethod
    def set(packet, bit_array):
        """
        Sets the protocol bit(s) for the passed in packet
        :param packet:          the packet to manipulate
        :param bit_array:       array of bits to be inserted
        """
        pass

    @staticmethod
    def get(packet, bits=0):
        """
        Retrieves the value of the bits for the field the protocol operates on
        :param packet:      the packet to retrieve information from
        :param bits:        number of bits to retrieve. Default value 0 means all
        :return:            array of bits retrieved from the packet
        """

