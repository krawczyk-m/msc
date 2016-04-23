

class BitConverter(object):
    """
    Provides conversion between a bit array and integers
    """

    @staticmethod
    def int(bit_array):
        out = 0
        for bit in bit_array:
            out = (out << 1) | bit
        return out

    @staticmethod
    def bit_array(integer):
        return [1 if digit == '1' else 0 for digit in bin(integer)[2:]]