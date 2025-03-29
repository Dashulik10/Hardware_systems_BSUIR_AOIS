import unittest
from unittest.mock import MagicMock
from logical_processing.expression_validator import ExpressionValidator
from logical_processing.min import Minimizing
from logical_processing.KarnaughMinimizer import KarnaughMinimizer


class TestKarnaughMinimizer(unittest.TestCase):
    def setUp(self):
        self.expression = "a & b | !a & c"
        self.minimizer = KarnaughMinimizer(self.expression)

        self.mock_truth_table_generator = MagicMock()
        self.minimizer.truth_table_generator = self.mock_truth_table_generator
        ExpressionValidator.VARIABLES = {"a", "b", "c", "d"} 

    def test_generate_simplified_table(self):
        self.mock_truth_table_generator.generate_table.return_value = [
            ({"a": 0, "b": 0, "c": 0}, None, 0),
            ({"a": 0, "b": 0, "c": 1}, None, 1),
            ({"a": 0, "b": 1, "c": 0}, None, 1),
            ({"a": 1, "b": 0, "c": 0}, None, 1),
        ]

        expected_table = [
            [0, 0, 0, 0],
            [0, 0, 1, 1],
            [0, 1, 0, 1],
            [1, 0, 0, 1]
        ]

        simplified_table = self.minimizer.generate_simplified_table()
        self.assertEqual(simplified_table, expected_table)

    def test_generate_karnaugh_map(self):
        self.mock_truth_table_generator.generate_table.return_value = [
            ({"a": 0, "b": 0, "c": 0}, None, 0),
            ({"a": 0, "b": 0, "c": 1}, None, 1),
            ({"a": 1, "b": 1, "c": 0}, None, 1),
            ({"a": 1, "b": 1, "c": 1}, None, 0),
        ]

        expected_karnaugh_map = {
            "rows": [[0], [1]],
            "columns": [[0, 0], [0, 1], [1, 1], [1, 0]],
            "map": [
                [0, 1, None, None],
                [None, None, 0, 1]
            ]
        }

        kmap = self.minimizer.generate_karnaugh_map()
        self.assertEqual(kmap, expected_karnaugh_map)

    def test_find_group(self):
        kmap = [[1, 1], [1, 1]]
        rows = [[0], [1]]
        columns = [[0], [1]]
        used_cells = set()

        group = self.minimizer._find_group_d(0, 0, size=4, kmap=kmap, rows=rows, columns=columns, used_cells=used_cells)
        expected_group = {(0, 0), (0, 1), (1, 0), (1, 1)}
        self.assertEqual(group, expected_group)

    def test_minimize_sdnf(self):
        self.minimizer.generate_karnaugh_map = MagicMock(return_value={
            "rows": [[0], [1]],
            "columns": [[0, 0], [0, 1], [1, 1], [1, 0]],
            "map": [
                [0, 1, 0, 1],
                [1, 1, 0, 1]
            ]
        })

        result = self.minimizer.minimize_sdnf()
        expected_result = "(!b & c) | (b & !c) | (a & !b)"
        self.assertEqual(result, expected_result)

    def test_group_to_expression(self):
        group = {(0, 0), (0, 1), (1, 0), (1, 1)}
        rows = [[0], [1]]
        columns = [[0, 0], [0, 1]]
        result = self.minimizer._group_to_expression_d(group, rows, columns)
        expected_result = ['!b'] 
        self.assertEqual(result, expected_result)

        group = {(0, 0), (0, 1)}
        result = self.minimizer._group_to_expression_d(group, rows, columns)
        expected_result = ['!a', '!b'] 
        self.assertEqual(result, expected_result)

    def test_invalid_karnaugh_map(self):
        self.minimizer.variables = ["a"] 
        with self.assertRaises(ValueError):
            self.minimizer.generate_karnaugh_map()

        self.minimizer.variables = ["a", "b", "c", "d", "e", "f"] 
        with self.assertRaises(ValueError):
            self.minimizer.generate_karnaugh_map()

class TestMinimizing(unittest.TestCase):

    def setUp(self):
        self.variables = ['a', 'b', 'c']
        self.expression_sdnf = "(a & b & c) | (!a & b & !c) | (a & !b & c)"
        self.expression_sknf = "(a | b | !c) & (!a | b | c) & (a | !b | c)"
        self.terms_sdnf = [[1, 1, 1], [0, 1, 0], [1, 0, 1]]
        self.terms_sknf = [[1, 1, 0], [0, 1, 1], [1, 0, 1]]

        self.minimizer = KarnaughMinimizer(self.expression_sknf)

        self.mock_truth_table_generator = MagicMock()
        self.minimizer.truth_table_generator = self.mock_truth_table_generator

    def test_terms_sdnf(self):
        result = Minimizing.terms_sdnf(self.expression_sdnf)
        self.assertEqual(result, self.terms_sdnf)

    def test_term_to_expression_sdnf(self):
        term = [1, 0, 1]  # a & !b & c
        result = Minimizing.term_to_expression_sdnf(term, self.variables)
        self.assertEqual(result, "a & !b & c")

    def test_terms_sknf(self):
        result = Minimizing.terms_sknf(self.expression_sknf)
        self.assertEqual(result, self.terms_sknf)

    def test_term_to_expression_sknf(self):
        term = [1, 0, 1]  # a | !b | c
        result = Minimizing.term_to_expression_sknf(term, self.variables)
        self.assertEqual(result, "a | !b | c")

    def test_compare_terms_sdnf(self):
        terms = [[1, 1, 1], [1, 1, 0], [1, 0, 1], [0, 0, 1]]
        result = Minimizing.compare_terms_sdnf(terms, self.variables)
        expected = [[1, 1, 'X'], [1, 'X', 1], ['X', 0, 1]]
        self.assertEqual(result, expected)

    def test_minimize_sdnf(self):
        result = Minimizing.minimize_sdnf(self.expression_sdnf, self.variables)
        expected = [[1, 'X', 1], [0, 1, 0]]
        self.assertEqual(result, expected)

    def test_minimize_sdnf_second(self):
        result = Minimizing.minimize_sdnf_second(self.expression_sdnf, self.variables)
        expected = [[1, 'X', 1], [0, 1, 0]]
        self.assertEqual(result, expected)

    def test_minimize_sknf_second(self):
        result = Minimizing.minimize_sknf_second(self.expression_sknf, self.variables)
        expected = [[1, 1, 0], [0, 1, 1], [1, 0, 1]]
        self.assertEqual(result, expected)



    def test_minimize_sknf(self):
        self.minimizer.generate_karnaugh_map = MagicMock(return_value={
            "rows": [[0], [1]],
            "columns": [[0, 0], [0, 1], [1, 1], [1, 0]],
            "map": [
                [1, 0, 0, 1],
                [0, 1, 1, 0]
            ]
        })
        
        
        result = self.minimizer.minimize_sknf()
        expected_result = "(a | !c) & (!a | c)"
        self.assertEqual(result, expected_result)

    def test_find_group_k(self):
        kmap = [[0, 0], [0, 1]]  
        rows = [[0], [1]]
        columns = [[0], [1]]
        used_cells = set() 

        group = self.minimizer._find_group_k(0, 0, size=2, kmap=kmap, rows=rows, columns=columns, used_cells=used_cells)
        expected_group = {(0, 0), (0, 1)}  
        self.assertEqual(group, expected_group)

    def test_group_to_expression_k(self):
        group = {(0, 0), (0, 1)}
        rows = [[0], [1]]
        columns = [[0, 0], [0, 1]]
        result = self.minimizer._group_to_expression_k(group, rows, columns, sknf=True)
        expected_result = ["a", "b"] 
        self.assertEqual(result, expected_result)

        group = {(1, 0), (1, 1)}
        result = self.minimizer._group_to_expression_k(group, rows, columns, sknf=True)
        expected_result = ["!a", "b"]
        self.assertEqual(result, expected_result)

    def test_full_minimize_sknf_process(self):
        self.mock_truth_table_generator.generate_table.return_value = [
            ({"a": 0, "b": 0, "c": 0}, None, 1), 
            ({"a": 0, "b": 0, "c": 1}, None, 0),
            ({"a": 1, "b": 1, "c": 0}, None, 0), 
            ({"a": 1, "b": 1, "c": 1}, None, 1),
        ]

        expected_result = "(a | b | !c) & (!a | !b | c)" 

        self.minimizer.generate_table()
        result = self.minimizer.minimize_sknf()
        self.assertEqual(result, expected_result)
class TestMinimizeSKNF(unittest.TestCase):
    def setUp(self):
        self.variables = ["a", "b", "c"]

    def test_minimize_sknf_simple(self):
        expression = "(a | b | !c) & (!a | !b | c)"
        result = Minimizing.minimize_sknf(expression, self.variables)

        expected = [[1, 1, 0], [0, 0, 1]]
        self.assertEqual(result, expected)


    def test_minimize_sknf_from_terms(self):
        terms = [[1, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1]]
        result = Minimizing.minimize_sknf(terms, self.variables)

        expected = [['X', 0, 1], [0, 'X', 1], [1, 1, 0]]
        self.assertEqual(result, expected)

    def test_minimize_sknf_with_redundant_terms(self):
        expression = "(a | b | !c) & (!a | b | c) & (a | !b | c)"
        result = Minimizing.minimize_sknf(expression, self.variables)

        expected = [[1, 1, 0], [0, 1, 1], [1, 0, 1]]
        self.assertEqual(result, expected)

    def test_minimize_sknf_no_reduction(self):
        expression = "(a | b | !c) & (a | b | c)"
        result = Minimizing.minimize_sknf(expression, self.variables)

        expected = [[1, 1, 'X']]
        self.assertEqual(result, expected)

    def test_minimize_sknf_long_expression(self):
        expression = "(a | b | c) & (!a | b | c) & (a | !b | c) & (!a | !b | !c)"
        result = Minimizing.minimize_sknf(expression, self.variables)

        expected = [['X', 1, 1], [1, 'X', 1], [0, 0, 0]]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()

