import unittest
from scapy.layers.inet import IP

from protocols.IPIdentification import IPIdentification


class IPIdentificationTest(unittest.TestCase):

    def setUp(self):
        self.packet = IP()
        self.packet.id = 2**16 - 1  # max for the field

    def test_set_zero(self):
        modified = IPIdentification.set(self.packet, [0])
        self.assertEqual(0, modified.id)

    def test_set_one(self):
        modified = IPIdentification.set(self.packet, [1])
        self.assertEqual(1, modified.id)

    def test_set_one_2(self):
        modified = IPIdentification.set(self.packet, [0, 1])
        self.assertEqual(1, modified.id)

    def test_set_63(self):
        modified = IPIdentification.set(self.packet, [0, 0, 1, 1, 1, 1, 1, 1])
        self.assertEqual(63, modified.id)

    def test_set_max_less_1(self):
        array = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
        modified = IPIdentification.set(self.packet, array)
        self.assertEqual(2**16 - 2, modified.id)

    def test_get_(self):
        array = [1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1]
        modified = IPIdentification.set(self.packet, array)
        retrieved_array = IPIdentification.get(modified)

        self.assertEqual(retrieved_array, array)