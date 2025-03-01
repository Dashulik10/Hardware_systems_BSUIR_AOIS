class NormalForms:
    def __init__(self, truth_table, variables):
        self.table = truth_table
        self.variables = variables

    def get_sdnf(self):
        terms = []
        for row in self.table:
            if row[-1] == 1: # ищем где функция истинная
                term = [f"{var}" if val else f"!{var}" for var, val in zip(self.variables, row[:-1])] #создаем выражение
                terms.append(f"({' & '.join(term)})") # добавляем дизъюнкцию
        return " | ".join(terms)

    def get_sknf(self): # также, но уже с 0
        terms = []
        for row in self.table:
            if row[-1] == 0:
                term = [f"!{var}" if val else f"{var}" for var, val in zip(self.variables, row[:-1])]
                terms.append(f"({' | '.join(term)})")
        return " & ".join(terms)

    def get_numeric_sdnf(self):
        return "{" + ", ".join(str(i) for i, row in enumerate(self.table) if row[-1] == 1) + "}"

    def get_numeric_sknf(self):
        return "{" + ", ".join(str(i) for i, row in enumerate(self.table) if row[-1] == 0) + "}"
