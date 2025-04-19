from logical_processing.expression_validator import ExpressionValidator
from logical_processing.table import TruthTableWithSubexpressions


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

    def find_all_groups(self, for_sdnf=True):
        kmap = self.generate_karnaugh_map()
        rows = kmap["rows"]
        columns = kmap["columns"]
        karnaugh_map = kmap["map"]

        all_groups = []

        print("\n=== Поиск всех возможных групп ===")

        target_value = 1 if for_sdnf else 0

        num_rows = len(rows)
        num_cols = len(columns)

        for size in [32, 16, 8, 4, 2, 1]:
            for row in range(num_rows):
                for col in range(num_cols):
                    potential_group = self._find_group(row, col, size, karnaugh_map, rows, columns, target_value)
                    if potential_group:
                        print(f"Найдена группа размера {size}: {sorted(potential_group)}")
                        all_groups.append(sorted(potential_group))

        print("\nВсе группы:")
        for group in all_groups:
            print(group)

        return all_groups

    def _find_group(self, row, col, size, kmap, rows, columns, target_value):
        num_rows = len(rows)
        num_cols = len(columns)

        group = set()

        if size == 8:
            group_1x8 = {(row, (col + x) % num_cols) for x in range(8)}
            group_2x4 = {
                ((row + x) % num_rows, (col + y) % num_cols)
                for x in range(2) for y in range(4)
            }
            group_4x2 = {
                ((row + x) % num_rows, (col + y) % num_cols)
                for x in range(4) for y in range(2)
            }

            if len(group_2x4) == 8 and all(kmap[r][c] == target_value for r, c in group_2x4):
                group = group_2x4
            elif len(group_4x2) == 8 and all(kmap[r][c] == target_value for r, c in group_4x2):
                group = group_4x2
            elif len(group_1x8) == 8 and all(kmap[r][c] == target_value for r, c in group_1x8):
                group = group_1x8

        elif size == 16:
            group_2x8 = {
                ((row + x) % num_rows, (col + y) % num_cols)
                for x in range(2) for y in range(8)
            }
            group_4x4 = {
                ((row + x) % num_rows, (col + y) % num_cols)
                for x in range(4) for y in range(4)
            }
            if len(group_4x4) == 16 and all(kmap[r][c] == target_value for r, c in group_4x4):
                print(f"Группа 4x4 проходит: {[kmap[r][c] for r, c in group_4x4]}")
                group = group_4x4
            elif len(group_2x8) == 16 and all(kmap[r][c] == target_value for r, c in group_2x8):
                print(f"Группа 2x8 проходит: {[kmap[r][c] for r, c in group_2x8]}")
                group = group_2x8

        elif size == 32:
            group = {
                ((row + x) % num_rows, (col + y) % num_cols)
                for x in range(num_rows) for y in range(num_cols)
            }
            if not all(kmap[r][c] == target_value for r, c in group):
                group = set()

        elif size == 4:
            group_horizontal = {
                (row % num_rows, (col + x) % num_cols) for x in range(4)
            }
            group_vertical = {
                ((row + x) % num_rows, col % num_cols) for x in range(4)
            }

            if all(kmap[r][c] == target_value for r, c in group_horizontal) and len(group_horizontal) == 4:
                group = group_horizontal
            elif all(kmap[r][c] == target_value for r, c in group_vertical) and len(group_vertical) == 4:
                group = group_vertical

        elif size == 2:
            group_horizontal = {
                (row % num_rows, (col + x) % num_cols) for x in range(2)
            }
            group_vertical = {
                ((row + x) % num_rows, col % num_cols) for x in range(2)
            }

            if all(kmap[r][c] == target_value for r, c in group_horizontal) and len(group_horizontal) == 2:
                group = group_horizontal
            elif all(kmap[r][c] == target_value for r, c in group_vertical) and len(group_vertical) == 2:
                group = group_vertical

        elif size == 1:
            group = {(row % num_rows, col % num_cols)}

        if len(group) == size and all(kmap[r][c] == target_value for r, c in group):
            return group

        return None

    def filter_groups(self, groups, for_sdnf=True):
        kmap = self.generate_karnaugh_map()
        rows = kmap["rows"]
        columns = kmap["columns"]

        target_value = 1 if for_sdnf else 0

        covered_cells = set()

        sorted_groups = sorted(groups, key=len, reverse=True)

        final_groups = []

        print("\n=== Начинаем фильтрацию групп ===")

        for group in sorted_groups:
            uncovered_cells = [cell for cell in group if cell not in covered_cells]

            # Логируем состояние группы
            #print(f"\nРассматриваем группу: {group}")
            #print(f"Непокрытые клетки в этой группе: {uncovered_cells}")

            if uncovered_cells:
                #print(f"Добавляем группу {group} в финальный список.")
                final_groups.append(group)

                covered_cells.update(group)
                #print(f"Обновлено покрытие клеток: {sorted(covered_cells)}")
            #else:
                #print(f"Пропускаем группу {group}, так как все её клетки уже покрыты.")

        print("\n=== Фильтрация завершена ===")
        print(f"Финальные группы: {final_groups}")

        return final_groups

    def generate_implicant(group, variable_names, for_sdnf=True):
        num_variables = len(variable_names)
        stable_variables = []

        for i in range(num_variables):
            values = {code[i] for code in group}
            if len(values) == 1:
                value = values.pop()
                if for_sdnf:

                    if value == 0:
                        stable_variables.append(f"!{variable_names[i]}")
                    else:
                        stable_variables.append(variable_names[i])
                else:
                    if value == 1:
                        stable_variables.append(f"!{variable_names[i]}")
                    else:
                        stable_variables.append(variable_names[i])

        separator = "&" if for_sdnf else " | "
        return separator.join(stable_variables)

    def _coords_to_binary(self, row, col):
        kmap = self.generate_karnaugh_map()
        rows = kmap["rows"]
        columns = kmap["columns"]
        return rows[row] + columns[col]

    def _coords_to_binary(self, row, col):
        kmap = self.generate_karnaugh_map()
        rows = kmap["rows"]
        columns = kmap["columns"]
        return rows[row] + columns[col]

