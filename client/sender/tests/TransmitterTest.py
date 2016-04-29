import unittest
from scapy.layers.inet import IP
from client.sender.transmitter import Transmitter
from protocols.IPIdentification import IPIdentification


class TransmitterTest(unittest.TestCase):

    def setUp(self):
        self.packet = IP()
        # for IPIdentification mangling
        self.packet.id = 2**16 - 1  # max for the field
        self.transmitter = Transmitter(protocols=[IPIdentification])

    def test_round_trip_single(self):
        bit_array = [1, 0, 0, 1, 1]
        self.packet = self.transmitter.embed(self.packet, bit_array)
        retrieved_bit_array = self.transmitter.extract(self.packet)

        self.assertEqual(retrieved_bit_array, bit_array)
