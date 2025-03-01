import unittest

from logical_processing.table import TruthTable


class TestTruthTable(unittest.TestCase):
    def test_generate_truth_table(self):
        tt = TruthTable("a and not b", ['a', 'b'])
        expected_table = [
            (0, 0, 0),
            (0, 1, 0),
            (1, 0, 1),
            (1, 1, 0)
        ]
        self.assertEqual(tt.generate(), expected_table)


if __name__ == "__main__":
    unittest.main()
