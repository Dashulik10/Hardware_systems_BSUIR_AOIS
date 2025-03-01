import unittest
from logical_processing.normal_forms import NormalForms


class TestNormalForms(unittest.TestCase):
    def test_sdnf(self):
        truth_table = [
            (0, 0, 0),
            (0, 1, 1),
            (1, 0, 1),
            (1, 1, 0)
        ]
        variables = ['a', 'b']
        nf = NormalForms(truth_table, variables)

        expected_sdnf = "(!a & b) | (a & !b)"
        self.assertEqual(nf.get_sdnf(), expected_sdnf)

    def test_sknf(self):
        truth_table = [
            (0, 0, 0),
            (0, 1, 1),
            (1, 0, 1),
            (1, 1, 0)
        ]
        variables = ['a', 'b']
        nf = NormalForms(truth_table, variables)

        expected_sknf = "(a | b) & (!a | !b)"
        self.assertEqual(nf.get_sknf(), expected_sknf)

    def test_numeric_sdnf(self):
        truth_table = [
            (0, 0, 0),
            (0, 1, 1),
            (1, 0, 1),
            (1, 1, 0)
        ]
        variables = ['a', 'b']
        nf = NormalForms(truth_table, variables)
        expected_numeric_sdnf = "{1, 2}"
        self.assertEqual(nf.get_numeric_sdnf(), expected_numeric_sdnf)

    def test_numeric_sknf(self):
        truth_table = [
            (0, 0, 0),
            (0, 1, 1),
            (1, 0, 1),
            (1, 1, 0)
        ]
        variables = ['a', 'b']
        nf = NormalForms(truth_table, variables)
        expected_numeric_sknf = "{0, 3}"
        self.assertEqual(nf.get_numeric_sknf(), expected_numeric_sknf)


if __name__ == "__main__":
    unittest.main()