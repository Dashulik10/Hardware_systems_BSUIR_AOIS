import unittest
from binary_calculator.add_sub import AddSub


class TestAddSub(unittest.TestCase):

    def test_add_additional_positive(self):
        add_sub = AddSub(5, 3, bits=8)
        result_decimal, result_additional = add_sub.add_additional()
        self.assertEqual(result_decimal, 8)
        self.assertEqual(result_additional, "00001000")

    def test_add_additional_negative(self):
        add_sub = AddSub(-5, -3, bits=8)
        result_decimal, result_additional = add_sub.add_additional()
        self.assertEqual(result_decimal, -8)
        self.assertEqual(result_additional, "11111000")

    def test_add_additional_mixed(self):
        add_sub = AddSub(5, -2, bits=8)
        result_decimal, result_additional = add_sub.add_additional()
        self.assertEqual(result_decimal, 3)
        self.assertEqual(result_additional, "00000011")

        add_sub = AddSub(-5, 2, bits=8)
        result_decimal, result_additional = add_sub.add_additional()
        self.assertEqual(result_decimal, -3)
        self.assertEqual(result_additional, "11111101")

    def test_subtract_additional_positive(self):
        add_sub = AddSub(7, 4, bits=8)
        result_decimal, result_additional = add_sub.subtract_additional()
        self.assertEqual(result_decimal, 3)
        self.assertEqual(result_additional, "00000011")

    def test_subtract_additional_negative(self):
        add_sub = AddSub(4, 7, bits=8)
        result_decimal, result_additional = add_sub.subtract_additional()
        self.assertEqual(result_decimal, -3)
        self.assertEqual(result_additional, "11111101")

    def test_overflow_add_additional(self):
        add_sub = AddSub(100, 30, bits=8)
        with self.assertRaises(OverflowError):
            add_sub.add_additional()

        add_sub = AddSub(-100, -50, bits=8)
        with self.assertRaises(OverflowError):
            add_sub.add_additional()

    def test_additional_code(self):
        self.assertEqual(AddSub.additional_code(5, bits=8), "00000101")
        self.assertEqual(AddSub.additional_code(-5, bits=8), "11111011")
        self.assertEqual(AddSub.additional_code(0, bits=8), "00000000")


if __name__ == "__main__":
    unittest.main()


