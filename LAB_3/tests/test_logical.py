import unittest

from logical_processing.logic_evaluator import LogicEvaluator
from logical_processing.normal_forms import NormalForms
from logical_processing.expression_validator import ExpressionValidator
from logical_processing.table import TruthTableWithSubexpressions


class TestExpressionValidator(unittest.TestCase):
    def test_valid_expression(self):
        self.assertIsNone(ExpressionValidator.validate("a | b"))
        self.assertIsNone(ExpressionValidator.validate("(a & b) -> c"))
        self.assertIsNone(ExpressionValidator.validate("!a & (b | c)"))
        self.assertIsNone(ExpressionValidator.validate("(a -> b) & c | d"))

    def test_invalid_symbols(self):
        with self.assertRaises(ValueError) as context:
            ExpressionValidator.validate("a ? b")
        self.assertEqual(str(context.exception), "Недопустимый символ: ?")

        with self.assertRaises(ValueError) as context:
            ExpressionValidator.validate("x & y")
        self.assertEqual(str(context.exception), "Недопустимый символ: x")

    def test_consecutive_operators(self):
        with self.assertRaises(ValueError) as context:
            ExpressionValidator.validate("a & | b")
        self.assertEqual(str(context.exception), "Два оператора подряд недопустимы")

        with self.assertRaises(ValueError) as context:
            ExpressionValidator.validate("a || b")
        self.assertEqual(str(context.exception), "Два оператора подряд недопустимы")

    def test_invalid_operators(self):
        with self.assertRaises(ValueError) as context:
            ExpressionValidator.validate("a - b")
        self.assertEqual(str(context.exception), "Некорректный оператор: -")

        with self.assertRaises(ValueError) as context:
            ExpressionValidator.validate("a ->> b")
        self.assertEqual(str(context.exception), "Недопустимый символ: >")

    def test_unbalanced_parentheses(self):
        with self.assertRaises(ValueError) as context:
            ExpressionValidator.validate("(a & b")
        self.assertEqual(str(context.exception), "Несбалансированные скобки")

        with self.assertRaises(ValueError) as context:
            ExpressionValidator.validate("a & b)")
        self.assertEqual(str(context.exception), "Несбалансированные скобки")

        with self.assertRaises(ValueError) as context:
            ExpressionValidator.validate("(a & (b | c)) -> d)")
        self.assertEqual(str(context.exception), "Несбалансированные скобки")

    def test_empty_expression(self):
        with self.assertRaises(ValueError) as context:
            ExpressionValidator.validate("")
        self.assertEqual(str(context.exception), "Выражение не может быть пустым")

        with self.assertRaises(ValueError) as context:
            ExpressionValidator.validate(" ")
        self.assertEqual(str(context.exception), "Выражение не может быть пустым")

    def test_no_operator_between_variables(self):
        with self.assertRaises(ValueError) as context:
            ExpressionValidator.validate("a b")
        self.assertEqual(str(context.exception), "Между переменными должен быть оператор")

class TestLogicEvaluator(unittest.TestCase):
    def test_single_variable(self):
        evaluator = LogicEvaluator(["a"])
        self.assertTrue(evaluator.evaluate({"a": True}))
        self.assertFalse(evaluator.evaluate({"a": False}))

    def test_not_operator(self):
        evaluator = LogicEvaluator(["a", "!"])
        self.assertFalse(evaluator.evaluate({"a": True}))
        self.assertTrue(evaluator.evaluate({"a": False}))

    def test_and_operator(self):
        evaluator = LogicEvaluator(["a", "b", "&"])
        self.assertTrue(evaluator.evaluate({"a": True, "b": True}))
        self.assertFalse(evaluator.evaluate({"a": True, "b": False}))
        self.assertFalse(evaluator.evaluate({"a": False, "b": True}))
        self.assertFalse(evaluator.evaluate({"a": False, "b": False}))

    def test_or_operator(self):
        evaluator = LogicEvaluator(["a", "b", "|"])
        self.assertTrue(evaluator.evaluate({"a": True, "b": True}))
        self.assertTrue(evaluator.evaluate({"a": True, "b": False}))
        self.assertTrue(evaluator.evaluate({"a": False, "b": True}))
        self.assertFalse(evaluator.evaluate({"a": False, "b": False}))

    def test_implication_operator(self):
        evaluator = LogicEvaluator(["a", "b", "->"])
        self.assertTrue(evaluator.evaluate({"a": False, "b": False}))
        self.assertTrue(evaluator.evaluate({"a": False, "b": True}))
        self.assertFalse(evaluator.evaluate({"a": True, "b": False}))
        self.assertTrue(evaluator.evaluate({"a": True, "b": True}))

    def test_equivalence_operator(self):
        evaluator = LogicEvaluator(["a", "b", "~"])
        self.assertTrue(evaluator.evaluate({"a": True, "b": True}))
        self.assertTrue(evaluator.evaluate({"a": False, "b": False}))
        self.assertFalse(evaluator.evaluate({"a": True, "b": False}))
        self.assertFalse(evaluator.evaluate({"a": False, "b": True}))

    def test_complex_expression(self):
        evaluator = LogicEvaluator(["a", "b", "&", "c", "|"])
        self.assertTrue(evaluator.evaluate({"a": True, "b": True, "c": False}))
        self.assertTrue(evaluator.evaluate({"a": False, "b": True, "c": True}))
        self.assertFalse(evaluator.evaluate({"a": False, "b": False, "c": False}))
        self.assertTrue(evaluator.evaluate({"a": True, "b": True, "c": True}))

    def test_nested_operations(self):
        evaluator = LogicEvaluator(["a", "b", "|", "c", "!", "&"])
        self.assertFalse(evaluator.evaluate({"a": False, "b": False, "c": True}))
        self.assertTrue(evaluator.evaluate({"a": True, "b": False, "c": False}))
        self.assertTrue(evaluator.evaluate({"a": False, "b": True, "c": False}))
        self.assertFalse(evaluator.evaluate({"a": True, "b": False, "c": True}))

    def test_empty_rpn(self):
        evaluator = LogicEvaluator([])
        with self.assertRaises(IndexError):
            evaluator.evaluate({})

    def test_unknown_variable(self):
        evaluator = LogicEvaluator(["a", "b", "&"])
        with self.assertRaises(KeyError):
            evaluator.evaluate({"a": True})


class TestNormalForms(unittest.TestCase):
    def test_single_variable(self):
        variables = ["a"]
        truth_table = [
            ({"a": False}, 0, False),
            ({"a": True}, 1, True)
        ]
        normal_forms = NormalForms(truth_table, variables).compute()

        self.assertEqual(normal_forms["СКНФ"], "(a)")
        self.assertEqual(normal_forms["СДНФ"], "(a)")
        self.assertEqual(normal_forms["СКНФ Индексы"], [0])
        self.assertEqual(normal_forms["СДНФ Индексы"], [1])

    def test_double_variables(self):
        variables = ["a", "b"]
        truth_table = [
            ({"a": False, "b": False}, 0, False),
            ({"a": False, "b": True}, 1, False),
            ({"a": True, "b": False}, 2, True),
            ({"a": True, "b": True}, 3, True)
        ]
        normal_forms = NormalForms(truth_table, variables).compute()

        self.assertEqual(normal_forms["СКНФ"], "(a | b) & (a | !b)")
        self.assertEqual(normal_forms["СДНФ"], "(a & !b) | (a & b)")
        self.assertEqual(normal_forms["СКНФ Индексы"], [0, 1])
        self.assertEqual(normal_forms["СДНФ Индексы"], [2, 3])

    def test_triple_variables(self):
        variables = ["x", "y", "z"]
        truth_table = [
            ({"x": False, "y": False, "z": False}, 0, False),
            ({"x": False, "y": False, "z": True}, 1, True),
            ({"x": False, "y": True, "z": False}, 2, False),
            ({"x": False, "y": True, "z": True}, 3, True),
            ({"x": True, "y": False, "z": False}, 4, False),
            ({"x": True, "y": False, "z": True}, 5, True),
            ({"x": True, "y": True, "z": False}, 6, False),
            ({"x": True, "y": True, "z": True}, 7, True)
        ]
        normal_forms = NormalForms(truth_table, variables).compute()

        self.assertEqual(normal_forms["СКНФ"], "(x | y | z) & (x | !y | z) & (!x | y | z) & (!x | !y | z)")
        self.assertEqual(normal_forms["СДНФ"],
                         "(!x & !y & z) | (!x & y & z) | (x & !y & z) | (x & y & z)")
        self.assertEqual(normal_forms["СКНФ Индексы"], [0, 2, 4, 6])
        self.assertEqual(normal_forms["СДНФ Индексы"], [1, 3, 5, 7])

    def test_empty_truth_table(self):
        variables = []
        truth_table = []
        normal_forms = NormalForms(truth_table, variables).compute()

        self.assertEqual(normal_forms["СКНФ"], "")
        self.assertEqual(normal_forms["СДНФ"], "")
        self.assertEqual(normal_forms["СКНФ Индексы"], [])
        self.assertEqual(normal_forms["СДНФ Индексы"], [])

    def test_all_false(self):
        variables = ["p"]
        truth_table = [
            ({"p": False}, 0, False),
            ({"p": True}, 1, False)
        ]
        normal_forms = NormalForms(truth_table, variables).compute()

        self.assertEqual(normal_forms["СКНФ"], "(p) & (!p)")
        self.assertEqual(normal_forms["СДНФ"], "")
        self.assertEqual(normal_forms["СКНФ Индексы"], [0, 1])
        self.assertEqual(normal_forms["СДНФ Индексы"], [])

    def test_all_true(self):
        variables = ["q"]
        truth_table = [
            ({"q": False}, 0, True),
            ({"q": True}, 1, True)
        ]
        normal_forms = NormalForms(truth_table, variables).compute()

        self.assertEqual(normal_forms["СКНФ"], "")
        self.assertEqual(normal_forms["СДНФ"], "(!q) | (q)")
        self.assertEqual(normal_forms["СКНФ Индексы"], [])
        self.assertEqual(normal_forms["СДНФ Индексы"], [0, 1])


class TestTruthTableWithSubexpressions(unittest.TestCase):
    def setUp(self):
        ExpressionValidator.OPERATORS = {"!": 3, "&": 2, "|": 2, "->": 1, "~": 1}
        ExpressionValidator.VARIABLES = {"a", "b", "c", "d", "e"}

    def test_extract_subexpressions(self):
        table = TruthTableWithSubexpressions("a & b | c")
        table.extract_subexpressions()

        expected_subexpressions = ['(a & b)', '((a & b) | c)']
        self.assertEqual(table.subexpression_strs, expected_subexpressions)

    def test_generate_table(self):
        table = TruthTableWithSubexpressions("a & !b")
        truth_table = table.generate_table()

        expected_table = [
            ({"a": False, "b": False}, [True, False], False),
            ({"a": False, "b": True}, [False, False], False),
            ({"a": True, "b": False}, [True, True], True),
            ({"a": True, "b": True}, [False, False], False),
        ]
        self.assertEqual(truth_table, expected_table)

    def test_evaluate_subexpressions(self):
        table = TruthTableWithSubexpressions("a & (b | c)")
        table.extract_subexpressions()

        variable_values = {"a": True, "b": False, "c": True}

        subformula_results, final_result = table.evaluate_subexpressions(variable_values)
        self.assertEqual(subformula_results, [True, True])
        self.assertEqual(final_result, True)

    def test_to_index_form(self):
        table = TruthTableWithSubexpressions("a & !b")
        index_form = table.to_index_form()

        expected_binary = "0010"
        expected_decimal = 2
        self.assertEqual(index_form["binary"], expected_binary)
        self.assertEqual(index_form["decimal"], expected_decimal)

    def test_display_table(self):
        table = TruthTableWithSubexpressions("a | b")
        try:
            table.display_table()
        except Exception as e:
            self.fail(f"display_table вызвал ошибку: {e}")

if __name__ == "__main__":
    unittest.main()
