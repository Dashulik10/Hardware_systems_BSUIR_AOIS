class TruthTable:
    def __init__(self, expression, variables):
        self.expression = expression
        self.variables = variables
        self.table = []

    def generate(self):
        num_vars = len(self.variables)
        num_rows = 2 ** num_vars

        for i in range(num_rows): # если 3 переменные то я от 1 до 8 беру числа и превращаю их в бинарку
            values = self._decimal_to_binary_list(i, num_vars) # и есть перевод
            context = dict(zip(self.variables, values)) # сразу сопоставляем значение и бинарку
            result = eval(self.expression, {}, context) # строчку обрабатываем как выражение, глобальные переменные не используются
            self.table.append((*values, int(result)))

        return self.table

    def _decimal_to_binary_list(self, num, length):
        binary_str = bin(num)[2:].zfill(length) # обрезаем нули
        return [int(bit) for bit in binary_str] # создаем список преобраззованных в число 101

    def display(self):
        print(" | ".join(self.variables) + " | F")
        print("-" * (len(self.variables) * 4 + 4))
        for row in self.table:
            print(" | ".join(map(str, row)))
