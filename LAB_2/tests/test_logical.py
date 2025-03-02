import unittest
from logical_processing.expression_validator import ExpressionValidator
from logical_processing.rpn_converter import RPNConverter
from logical_processing.logic_evaluator import LogicEvaluator
from logical_processing.table import TruthTable
from logical_processing.normal_forms import NormalForms


class TestExpressionValidator(unittest.TestCase):
    def test_valid_expressions(self):
        valid_expressions = [
            "a & b",
            "a | !b",
            "a -> b",
            "(a & b) | c",
            "((a | b) & (!c -> d))"
        ]
        for expr in valid_expressions:
            try:
                ExpressionValidator.validate(expr)
            except ValueError:
                self.fail(f"ExpressionValidator raised ValueError for valid expression: {expr}")


class TestRPNConverter(unittest.TestCase):
    def test_to_rpn(self):
        expressions_and_rpn = [
            ("a & b", ["a", "b", "&"]),
            ("a | !b", ["a", "b", "!", "|"]),
            ("a -> b", ["a", "b", "->"]),
            ("(a & b) | c", ["a", "b", "&", "c", "|"]),
            ("!a & (b | c)", ["a", "!", "b", "c", "|", "&"]),
            ("a ~ b", ["a", "b", "~"])
        ]
        for expr, expected_rpn in expressions_and_rpn:
            converter = RPNConverter(expr)
            self.assertEqual(converter.to_rpn(), expected_rpn)


class TestLogicEvaluator(unittest.TestCase):
    def test_evaluate(self):
        cases = [
            (["a", "b", "&"], {"a": True, "b": True}, True),
            (["a", "b", "&"], {"a": True, "b": False}, False),
            (["a", "b", "|"], {"a": False, "b": True}, True),
            (["a", "!"], {"a": True}, False),
            (["a", "b", "->"], {"a": True, "b": False}, False),
            (["a", "b", "->"], {"a": False, "b": True}, True),
            (["a", "b", "~"], {"a": True, "b": True}, True),
            (["a", "b", "~"], {"a": True, "b": False}, False)
        ]
        for rpn, values, expected in cases:
            evaluator = LogicEvaluator(rpn)
            self.assertEqual(evaluator.evaluate(values), expected)


class TestTruthTable(unittest.TestCase):
    def test_generate_truth_table(self):
        expr = "a & b"
        truth_table = TruthTable(expr)
        expected_table = [
            ({"a": False, "b": False}, False),
            ({"a": False, "b": True}, False),
            ({"a": True, "b": False}, False),
            ({"a": True, "b": True}, True)
        ]
        self.assertEqual(truth_table.generate(), expected_table)

    def test_to_index_form(self):
        expr = "a & b"
        truth_table = TruthTable(expr)
        index_form = truth_table.to_index_form()
        self.assertEqual(index_form["binary"], "0001")
        self.assertEqual(index_form["decimal"], 1)


class TestNormalFormsInit(unittest.TestCase):
    def test_valid_initialization(self):
        truth_table = [
            ({"a": False, "b": False}, False),
            ({"a": True, "b": True}, True),
        ]
        variables = ["a", "b"]

        normal_forms = NormalForms(truth_table, variables)

        # Проверка атрибутов
        self.assertEqual(normal_forms.truth_table, truth_table)
        self.assertEqual(normal_forms.variables, variables)

    def test_empty_truth_table(self):
        truth_table = []
        variables = ["a", "b"]

        normal_forms = NormalForms(truth_table, variables)

        # Проверка атрибутов
        self.assertEqual(normal_forms.truth_table, truth_table)
        self.assertEqual(normal_forms.variables, variables)

    def test_empty_variables(self):
        truth_table = [
            ({"a": False}, False),
        ]
        variables = []

        normal_forms = NormalForms(truth_table, variables)

        # Проверка атрибутов
        self.assertEqual(normal_forms.truth_table, truth_table)
        self.assertEqual(normal_forms.variables, variables)

class TestNormalFormsCompute(unittest.TestCase):
    def setUp(self):
        self.variables = ["a", "b"]

    def test_compute_with_valid_truth_table(self):
        truth_table = [
            ({"a": False, "b": False}, False),
            ({"a": False, "b": True}, False),
            ({"a": True, "b": False}, False),
            ({"a": True, "b": True}, True)
        ]
        normal_forms = NormalForms(truth_table, self.variables)
        forms = normal_forms.compute()


    def test_compute_empty_truth_table(self):
        truth_table = []
        normal_forms = NormalForms(truth_table, self.variables)
        forms = normal_forms.compute()

        self.assertEqual(forms["СКНФ"], "")
        self.assertEqual(forms["СДНФ"], "")
        self.assertEqual(forms["СКНФ Индексы"], [])
        self.assertEqual(forms["СДНФ Индексы"], [])


if __name__ == "__main__":
    unittest.main()
