import unittest
from protocols.util.BitConverter import BitConverter


class BitConverterTest(unittest.TestCase):

    def test_to_int_conversion(self):
        self.assertEqual(0, BitConverter.int([0]))
        self.assertEqual(1, BitConverter.int([1]))
        self.assertEqual(1, BitConverter.int([0, 0, 1]))
        self.assertEqual(3, BitConverter.int([0, 1, 1]))
        self.assertEqual(5, BitConverter.int([1, 0, 1]))
        self.assertEqual(7, BitConverter.int([1, 1, 1]))
        self.assertEqual(255, BitConverter.int([1, 1, 1, 1, 1, 1, 1, 1]))
        self.assertEqual(1023, BitConverter.int([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]))

    def test_to_bit_array_conversion(self):
        self.assertEqual([0], BitConverter.bit_array(0))
        self.assertEqual([1], BitConverter.bit_array(1))
        self.assertEqual([1, 1], BitConverter.bit_array(3))
        self.assertEqual([1, 0, 1], BitConverter.bit_array(5))
        self.assertEqual([1, 1, 1], BitConverter.bit_array(7))
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1], BitConverter.bit_array(255))
        self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1, 1, 0], BitConverter.bit_array(1022))