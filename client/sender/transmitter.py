
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

    def embed(self, packet):
        pass

    def extract(self, packet):
        pass
