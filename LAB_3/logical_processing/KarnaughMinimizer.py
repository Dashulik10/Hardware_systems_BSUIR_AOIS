from logical_processing.expression_validator import ExpressionValidator
from logical_processing.table import TruthTableWithSubexpressions
from logical_processing.min import Minimizing


class KarnaughMinimizer:
    def __init__(self, expression):
        self.expression = expression
        self.variables = sorted(ExpressionValidator.VARIABLES & set(expression))
        self.truth_table_generator = TruthTableWithSubexpressions(expression)
        self.truth_table = []

    def generate_table(self):
        self.truth_table = self.truth_table_generator.generate_table()

    def display_simplified_table(self):
        simplified_table = self.generate_simplified_table()

        headers = self.variables + ["Result"]
        header_row = " | ".join(headers)
        print(header_row)
        print("-" * len(header_row))

        for row in simplified_table:
            print(" | ".join(map(str, row)))

    def generate_simplified_table(self):
        table = self.truth_table_generator.generate_table()

        simplified_table = []
        for variable_values, _, final_result in table:
            combination = [int(variable_values[var]) for var in self.variables] 
            simplified_table.append(combination + [int(final_result)])  

        return simplified_table


    def generate_karnaugh_map(self):
        simplified_table = self.generate_simplified_table()
        num_vars = len(self.variables)

        if num_vars < 2 or num_vars > 5:
            raise ValueError("Таблицы Карно поддерживаются только для 2-5 переменных.")

        if num_vars <= 4:
            group_1_vars = self.variables[:num_vars // 2]
            group_2_vars = self.variables[num_vars // 2:]
        else:
            group_1_vars = self.variables[:2]
            group_2_vars = self.variables[2:]

        row_headers = self._generate_gray_code(len(group_1_vars))
        col_headers = self._generate_gray_code(len(group_2_vars))

        karnaugh_map = [
            [None for _ in col_headers]
            for _ in row_headers
        ]

        for row_header in range(len(row_headers)):
            for col_header in range(len(col_headers)):
                combination = row_headers[row_header] + col_headers[col_header]
                for entry in simplified_table:
                    if entry[:num_vars] == combination:
                        karnaugh_map[row_header][col_header] = entry[-1]

        return {
            "rows": row_headers,
            "columns": col_headers,
            "map": karnaugh_map
        }

    def display_karnaugh_map(self):
        kmap = self.generate_karnaugh_map()

        rows = kmap["rows"]
        columns = kmap["columns"]
        karnaugh_map = kmap["map"]

        num_vars = len(self.variables)
        if num_vars <= 4:
            row_vars = self.variables[:num_vars // 2]
            col_vars = self.variables[num_vars // 2:]
        else:
            row_vars = self.variables[:2]
            col_vars = self.variables[2:]

        print(f"Строки ({','.join(row_vars)})")
        print(f"Столбцы ({','.join(col_vars)})")
        print()

        cell_width = max(
            len("".join(map(str, col))) for col in (columns + rows)
        ) + 2

        col_header = " " * (len(row_vars) + 3)
        col_header += " | ".join(f"{''.join(map(str, col)):^{cell_width}}" for col in columns)
        print(col_header)
        print(" " * (len(row_vars) + 3) + "-" * (len(col_header) - (len(row_vars) + 3)))

        for row, values in zip(rows, karnaugh_map):
            row_header = "".join(map(str, row)).ljust(3)
            row_values = " | ".join(f"{str(v) if v is not None else '-':^{cell_width}}" for v in values)
            print(f"{row_header}{row_values}")

    @staticmethod
    def _generate_gray_code(num_bits):
        if num_bits == 0:
            return [[]]
        smaller = KarnaughMinimizer._generate_gray_code(num_bits - 1)
        return [[0] + code for code in smaller] + [[1] + code for code in reversed(smaller)]



    def minimize_sdnf(self):
        kmap = self.generate_karnaugh_map()
        rows = kmap["rows"]
        columns = kmap["columns"]
        karnaugh_map = kmap["map"]

        minimized_terms = []

        uncovered_cells = {
            (row, col)
            for row in range(len(rows))
            for col in range(len(columns))
            if karnaugh_map[row][col] == 1
        }

        for size in [4, 2, 1]:
            for row_idx in range(len(rows)):
                for col_idx in range(len(columns)):
                    if (row_idx, col_idx) not in uncovered_cells:
                        continue

                    group = self._find_group_d(row_idx, col_idx, size, karnaugh_map, rows, columns, uncovered_cells)
                    if group:
                        term = self._group_to_expression_d(group, rows, columns)
                        minimized_terms.append(term)

                        uncovered_cells -= group

        return " | ".join(
            f"({' & '.join(filter(None, term))})" for term in minimized_terms
        )

    def minimize_sknf(self):
        kmap = self.generate_karnaugh_map()
        rows = kmap["rows"]
        columns = kmap["columns"]
        karnaugh_map = kmap["map"]

        minimized_terms = []

        uncovered_cells = {
            (row, col)
            for row in range(len(rows))
            for col in range(len(columns))
            if karnaugh_map[row][col] == 0
        }

        for size in [4, 2, 1]:
            for row_idx in range(len(rows)):
                for col_idx in range(len(columns)):
                    if (row_idx, col_idx) not in uncovered_cells:
                        continue

                    group = self._find_group_k(row_idx, col_idx, size, karnaugh_map, rows, columns, uncovered_cells)
                    if group:
                        term = self._group_to_expression_k(group, rows, columns, sknf=True)  
                        minimized_terms.append(term)

                        uncovered_cells -= group

        return " & ".join(
            f"({' | '.join(filter(None, term))})" for term in minimized_terms
        )


    def _generate_term(self, row_values, col_values):
        term = []
        combined = row_values + col_values
        for idx, value in enumerate(combined):
            if value == 1:
                term.append(self.variables[idx])
            elif value == 0:
                term.append(f"!{self.variables[idx]}")
        return term

    def _perform_grouping(self, terms):
        grouped = []

        for term in terms:
            for i, existing_term in enumerate(grouped):
                if self._can_be_grouped(term, existing_term):
                    grouped[i] = self._combine_terms(term, existing_term)
                    break
            else:
                grouped.append(term)

        return grouped

    def _can_be_grouped(self, term1, term2):
        differences = 0
        for t1, t2 in zip(term1, term2):
            if t1 != t2:
                differences += 1
            if differences > 1:
                return False
        return True

    def _combine_terms(self, term1, term2):
        return [
            t1 if t1 == t2 else None
            for t1, t2 in zip(term1, term2)
        ]

    def _find_group_d(self, row, col, size, kmap, rows, columns, used_cells):
        num_rows = len(rows)
        num_cols = len(columns)

        if size == 4:
            group = {
                (row % num_rows, col % num_cols),
                (row % num_rows, (col + 1) % num_cols),
                ((row + 1) % num_rows, col % num_cols),
                ((row + 1) % num_rows, (col + 1) % num_cols),
            }
            if all(kmap[r][c] == 1 for r, c in group):
                return group
        if size == 2:
            group_horizontal = {
                (row % num_rows, col % num_cols),
                (row % num_rows, (col + 1) % num_cols),
            }
            if all(kmap[r][c] == 1 for r, c in group_horizontal):
                return group_horizontal

            group_vertical = {
                (row % num_rows, col % num_cols),
                ((row + 1) % num_rows, col % num_cols),
            }
            if all(kmap[r][c] == 1 for r, c in group_vertical):
                return group_vertical

        if size == 1:
            group_single = {(row % num_rows, col % num_cols)}
            if kmap[row % num_rows][col % num_cols] == 1:
                return group_single

        return None

    def _find_group_k(self, row, col, size, kmap, rows, columns, used_cells):
        num_rows = len(rows)
        num_cols = len(columns)

        if size == 4:
            group = {
                (row % num_rows, col % num_cols),
                (row % num_rows, (col + 1) % num_cols),
                ((row + 1) % num_rows, col % num_cols),
                ((row + 1) % num_rows, (col + 1) % num_cols),
            }
            if all(kmap[r][c] == 0 for r, c in group):
                return group

        if size == 2:
            group_horizontal = {
                (row % num_rows, col % num_cols),
                (row % num_rows, (col + 1) % num_cols),
            }
            if all(kmap[r][c] == 0 for r, c in group_horizontal):
                return group_horizontal

            group_vertical = {
                (row % num_rows, col % num_cols),
                ((row + 1) % num_rows, col % num_cols),
            }
            if all(kmap[r][c] == 0 for r, c in group_vertical):
                return group_vertical

        if size == 1:
            group_single = {(row % num_rows, col % num_cols)}
            if kmap[row % num_rows][col % num_cols] == 0:
                return group_single

        return None

    def _group_to_expression_d(self, group, rows, columns):
        num_vars = len(self.variables)
        fixed_values = [None] * num_vars

        for row, col in group:
            row_values = rows[row]
            col_values = columns[col]
            combined = row_values + col_values

            for i, value in enumerate(combined):
                if fixed_values[i] is None:
                    fixed_values[i] = value
                elif fixed_values[i] != value:
                    print(f"Переменная {self.variables[i]} сброшена (меняется в группе)")
                    fixed_values[i] = None

        term = []
        for i, var in enumerate(self.variables):
            if fixed_values[i] is not None:
                if fixed_values[i] == 1:
                    term.append(var)
                else:
                    term.append(f"!{var}")
        print(f"Сформирован терм: {term}")
        return term

    def _group_to_expression_k(self, group, rows, columns, sknf=False):
        num_vars = len(self.variables)
        fixed_values = [None] * num_vars

        for row, col in group:
            row_values = rows[row]
            col_values = columns[col]
            combined = row_values + col_values

            for i, value in enumerate(combined):
                if fixed_values[i] is None:
                    fixed_values[i] = value
                elif fixed_values[i] != value:
                    fixed_values[i] = None

        term = []
        for i, var in enumerate(self.variables):
            if fixed_values[i] is not None:
                if sknf:
                    if fixed_values[i] == 0:
                        term.append(var)
                    else:
                        term.append(f"!{var}")
                else:
                    if fixed_values[i] == 1:
                        term.append(var)
                    else:
                        term.append(f"!{var}")

        return term
