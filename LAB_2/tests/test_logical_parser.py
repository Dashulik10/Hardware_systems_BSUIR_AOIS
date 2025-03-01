import unittest

from logical_processing.logical_parser import LogicParser
from logical_processing.normal_forms import NormalForms
from logical_processing.table import TruthTable


class TestLogicParser(unittest.TestCase):
    def test_valid_expression(self):
        parser = LogicParser("a & b | !c")
        self.assertEqual(parser.parse(), "a  and  b  or   not c")

    def test_detect_variables(self):
        parser = LogicParser("c & d | !a")
        self.assertEqual(parser.variables, ['a', 'c', 'd'])


if __name__ == "__main__":
    unittest.main()
