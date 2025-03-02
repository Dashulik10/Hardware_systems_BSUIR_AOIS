import itertools

from logical_processing.expression_validator import ExpressionValidator
from logical_processing.logic_evaluator import LogicEvaluator
from logical_processing.rpn_converter import RPNConverter


class TruthTable:
    def __init__(self, expression):
        ExpressionValidator.validate(expression)
        converter = RPNConverter(expression)
        self.rpn = converter.to_rpn()
        self.variables = sorted(ExpressionValidator.VARIABLES & set(expression))
        self.evaluator = LogicEvaluator(self.rpn)

    def generate(self):
        table = []
        for values in itertools.product([False, True], repeat=len(self.variables)):
            values_dict = dict(zip(self.variables, values))
            result = self.evaluator.evaluate(values_dict)
            table.append((values_dict, result))
        return table

    def to_index_form(self):
        truth_table = self.generate()
        binary_representation = "".join(str(int(result)) for _, result in truth_table)
        decimal_value = int(binary_representation, 2)
        return {
            "binary": binary_representation,
            "decimal": decimal_value
        }
