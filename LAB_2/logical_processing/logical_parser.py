import re


class LogicParser:

    OPERATORS = {
        '&': 'and',
        '|': 'or',
        '!': 'not',
        '->': '<=',
        '~': '=='
    }
    ALLOWED_VARS = {'a', 'b', 'c', 'd', 'e'}

    def __init__(self, expression: str):
        self.expression = expression.strip()
        self.variables = sorted(set(re.findall(r'[a-e]', expression)))
        self.validate_expression()

    def validate_expression(self):
        if re.search(r"[^a-e\s&|!->~()]", self.expression):
            raise ValueError("Недопустимые символы!")

        if self.expression.count('(') != self.expression.count(')'):
            raise ValueError("Некорректное количество скобок!")

        if re.search(r"[\&\|\~\-]{2,}", self.expression.replace("->", "-")):
            raise ValueError("Два оператора подряд недопустимы!")

        if not any(var in self.expression for var in self.ALLOWED_VARS):
            raise ValueError("В выражении отсутствуют переменные!")

    def parse(self):
        parsed_expr = self.expression
        for operator, replacement in self.OPERATORS.items():
            parsed_expr = parsed_expr.replace(operator, f' {replacement} ')
        return parsed_expr
