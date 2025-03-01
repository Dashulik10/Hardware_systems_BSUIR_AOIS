import unittest
from binary_calculator.converter import Converter


class TestConverter(unittest.TestCase):

    def test_make_it_binary_positive(self):
        self.assertEqual(Converter(5, bits=8).make_it_binary(), "00000101")
        self.assertEqual(Converter(0, bits=8).make_it_binary(), "00000000")
        self.assertEqual(Converter(255, bits=8).make_it_binary(), "11111111")

    def test_make_it_binary_invalid(self):
        with self.assertRaises(ValueError):
            Converter(-1, bits=8).make_it_binary()

        with self.assertRaises(ValueError):
            Converter(-128, bits=8).make_it_binary()

    def test_direct_code_positive(self):
        self.assertEqual(Converter(5, bits=8).direct_code(), "0 0000101")
        self.assertEqual(Converter(0, bits=8).direct_code(), "0 0000000")
        self.assertEqual(Converter(127, bits=8).direct_code(), "0 1111111")

    def test_direct_code_negative(self):
        self.assertEqual(Converter(-5, bits=8).direct_code(), "1 0000101")
        self.assertEqual(Converter(-1, bits=8).direct_code(), "1 0000001")
        self.assertEqual(Converter(-127, bits=8).direct_code(), "1 1111111")

    def test_reverse_code_positive(self):
        self.assertEqual(Converter(5, bits=8).reverse_code(), "0 0000101")
        self.assertEqual(Converter(0, bits=8).reverse_code(), "0 0000000")

    def test_reverse_code_negative(self):
        self.assertEqual(Converter(-5, bits=8).reverse_code(), "1 1111010")
        self.assertEqual(Converter(-1, bits=8).reverse_code(), "1 1111110")
        self.assertEqual(Converter(-127, bits=8).reverse_code(), "1 0000000")

    def test_additional_code_positive(self):
        self.assertEqual(Converter(5, bits=8).additional_code(), "0 0000101")
        self.assertEqual(Converter(0, bits=8).additional_code(), "0 0000000")

    def test_additional_code_negative(self):
        self.assertEqual(Converter(-5, bits=8).additional_code(), "1 1111011")
        self.assertEqual(Converter(-1, bits=8).additional_code(), "1 1111111")
        self.assertEqual(Converter(-127, bits=8).additional_code(), "1 0000001")

    def test_edge_cases(self):
        self.assertEqual(Converter(0, bits=8).direct_code(), "0 0000000")
        self.assertEqual(Converter(0, bits=8).reverse_code(), "0 0000000")
        self.assertEqual(Converter(0, bits=8).additional_code(), "0 0000000")
        self.assertEqual(Converter(-128, bits=8).additional_code(), "1 0000000")



if __name__ == "__main__":
    unittest.main()
