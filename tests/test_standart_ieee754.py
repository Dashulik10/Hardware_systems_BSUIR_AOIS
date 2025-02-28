import unittest

from standart_ieee754 import StandartIEEE754


class TestStandartIEEE754(unittest.TestCase):
    def setUp(self):
        self.calc1 = StandartIEEE754(5.5, -2.75)
        self.calc2 = StandartIEEE754(0.0, 0.0)
        self.calc3 = StandartIEEE754(10.25, 20.5)

    def test_float_to_ieee754(self):
        self.assertEqual(self.calc1.float_to_ieee754(0.0), '0' * 32)
        self.assertEqual(self.calc1.float_to_ieee754(1.0), '00111111100000000000000000000000')
        self.assertEqual(self.calc1.float_to_ieee754(-1.0), '10111111100000000000000000000000')
        self.assertEqual(self.calc1.float_to_ieee754(2.5), '01000000001000000000000000000000')

    def test_ieee754_to_float(self):
        self.assertAlmostEqual(self.calc1.ieee754_to_float('00111111100000000000000000000000'), 1.0)
        self.assertAlmostEqual(self.calc1.ieee754_to_float('10111111100000000000000000000000'), -1.0)
        self.assertAlmostEqual(self.calc1.ieee754_to_float('01000000001000000000000000000000'), 2.5)

    def test_ieee754_addition(self):
        result_ieee = self.calc1.ieee754_addition()
        result_float = self.calc1.ieee754_to_float(result_ieee)
        self.assertAlmostEqual(result_float, 5.5 + (-2.75))

        result_ieee = self.calc3.ieee754_addition()
        result_float = self.calc3.ieee754_to_float(result_ieee)
        self.assertAlmostEqual(result_float, 10.25 + 20.5)

    def test_sum_of_binary_ieee754(self):
        result_ieee = self.calc1.sum_of_binary_ieee754()
        result_float = self.calc1.ieee754_to_float(result_ieee)
        self.assertAlmostEqual(result_float, 5.5 + (-2.75))

    def test_invalid_input_float_to_ieee754(self):
        with self.assertRaises(TypeError):
            self.calc1.float_to_ieee754("string")

    def test_invalid_input_ieee754_to_float(self):
        with self.assertRaises(ValueError):
            self.calc1.ieee754_to_float("invalid_binary_string")

    def test_invalid_input_ieee754_addition(self):
        with self.assertRaises(TypeError):
            StandartIEEE754("invalid", 2.5).ieee754_addition()

    def test_subnormal_case(self):
        self.assertEqual(self.calc1.float_to_ieee754(1e-40), '00000000000000000000000000000000')
        self.assertAlmostEqual(self.calc1.ieee754_to_float('00000000000000000000000000000001'), 1.4e-45)

    def test_zero_case(self):
        self.assertEqual(self.calc1.float_to_ieee754(0.0), '0' * 32)
        self.assertAlmostEqual(self.calc1.ieee754_to_float('00000000000000000000000000000000'), 0.0)


if __name__ == '__main__':
    unittest.main()