import unittest
from src.Matrix import Matrix


class TestMatrix(unittest.TestCase):
    def setUp(self):
        initial_matrix = [
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.matrix = Matrix(initial_matrix)

    def test_initial_matrix(self):
        self.assertEqual(self.matrix.rows, 16)
        self.assertEqual(self.matrix.cols, 16)
        self.assertEqual(self.matrix.read_word(0, 0), [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0])

    def test_read_word(self):
        self.assertEqual(self.matrix.read_word(0, 0), [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0])
        self.assertEqual(self.matrix.read_word(5, 3), [1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0])

    def test_write_word(self):
        word = [0] * 16
        self.matrix.write_word(word, 0, 0)
        self.assertEqual(self.matrix.read_word(0, 0), word)

    def test_read_diagonal_column(self):
        diagonal = self.matrix.read_diagonal_column(3)
        expected_diagonal = "1110110010010000"
        self.assertEqual(diagonal, expected_diagonal)

    def test_write_diagonal_column(self):
        new_column = ["1"] * self.matrix.rows
        self.matrix.write_diagonal_column(2, new_column)
        diagonal = self.matrix.read_diagonal_column(2)
        self.assertEqual(diagonal, "1111111111111111")

    def test_logical_operation(self):
        self.matrix.logical_operation("not", 7, 8, 10)
        result_word = self.matrix.read_word(0, 10)
        expected_result = [1 - bit for bit in self.matrix.read_word(0, 8)]
        self.assertEqual(result_word, expected_result)

        self.matrix.logical_operation("const_1", 0, 0, 0)
        result_word = self.matrix.read_word(0, 0)
        self.assertEqual(result_word, [1] * self.matrix.rows)

    def test_add_fields(self):
        self.matrix.add_fields([1, 1, 1])
        updated_word = self.matrix.read_word(0, 0)
        self.assertEqual(updated_word[11:], [0, 1, 1, 1, 1])

    def test_search_best_match(self):
        search_argument = [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0]
        best_matches = self.matrix.search_best_match(search_argument)

        self.assertEqual(len(best_matches), 1)
        self.assertEqual(best_matches[0][1], search_argument)


if __name__ == "__main__":
    unittest.main()