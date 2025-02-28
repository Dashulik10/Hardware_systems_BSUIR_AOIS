import unittest
from binary_calculator.operations import Operations


class TestOperations(unittest.TestCase):
    def test_multiply_direct(self):
        ops = Operations(3, -2, bits=8)
        result_decimal, result_direct = ops.multiply_direct()
        self.assertEqual(result_decimal, -6)
        self.assertEqual(result_direct, "10000110")

        ops = Operations(-4, -2, bits=8)
        result_decimal, result_direct = ops.multiply_direct()
        self.assertEqual(result_decimal, 8)
        self.assertEqual(result_direct, "00001000")

        with self.assertRaises(OverflowError):
            ops = Operations(3, 50, bits=8)
            ops.multiply_direct()

    def test_binary_divide(self):
        ops = Operations(6, 3, bits=8)
        decimal_value, res_binary = ops.binary_divide(precision=5)
        self.assertEqual(decimal_value, 2.0)
        self.assertEqual(res_binary, "010.00000")

        ops = Operations(-8, 4, bits=8)
        decimal_value, res_binary = ops.binary_divide(precision=5)
        self.assertEqual(decimal_value, -2.0)
        self.assertEqual(res_binary, "110.00000")

        with self.assertRaises(ZeroDivisionError):
            ops = Operations(5, 0, bits=8)
            ops.binary_divide()

    def test_edge_cases(self):
        ops = Operations(0, 3, bits=8)
        decimal_value, res_binary = ops.binary_divide(precision=5)
        self.assertEqual(decimal_value, 0.0)
        self.assertEqual(res_binary, "00.00000")

        ops = Operations(0, 5, bits=8)
        result_decimal, result_direct = ops.multiply_direct()
        self.assertEqual(result_decimal, 0)
        self.assertEqual(result_direct, "00000000")

    def test_direct_code_generation(self):
        ops = Operations(5, bits=8)
        self.assertEqual(ops.direct_code(5), "00000101")
        self.assertEqual(ops.direct_code(-5), "10000101")



if __name__ == "__main__":
    unittest.main()
