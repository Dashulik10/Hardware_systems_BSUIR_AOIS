from logical_processing.expression_validator import ExpressionValidator


class LogicEvaluator:
    def __init__(self, rpn_expression):
        self.rpn = rpn_expression

    def evaluate(self, values):
        stack = []
        for token in self.rpn:
            if token in ExpressionValidator.VARIABLES:
                stack.append(values[token])
            elif token == '!':
                stack.append(not stack.pop())
            elif token == '&':
                b, a = stack.pop(), stack.pop()
                stack.append(a and b)
            elif token == '|':
                b, a = stack.pop(), stack.pop()
                stack.append(a or b)
            elif token == '->':
                b, a = stack.pop(), stack.pop()
                stack.append(not a or b)
            elif token == '~':
                b, a = stack.pop(), stack.pop()
                stack.append(a == b)
        return stack[0]