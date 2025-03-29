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
        """
        Отображает таблицу, содержащую только комбинации переменных и итоговый результат.
        """
        simplified_table = self.generate_simplified_table()

        # Заголовки
        headers = self.variables + ["Result"]
        header_row = " | ".join(headers)
        print(header_row)
        print("-" * len(header_row))

        # Построчный вывод
        for row in simplified_table:
            print(" | ".join(map(str, row)))

    def generate_simplified_table(self):
        """
        Генерирует таблицу истинности, отображая только комбинации переменных и конечный результат.
        """
        table = self.truth_table_generator.generate_table()

        simplified_table = []
        for variable_values, _, final_result in table:
            combination = [int(variable_values[var]) for var in self.variables]  # Значения переменных
            simplified_table.append(combination + [int(final_result)])  # Добавляем результат

        return simplified_table














    def generate_karnaugh_map(self):
        """
        Генерирует таблицу Карно, поддерживая 2-5 переменных.
        """
        simplified_table = self.generate_simplified_table()
        num_vars = len(self.variables)

        if num_vars < 2 or num_vars > 5:
            raise ValueError("Таблицы Карно поддерживаются только для 2-5 переменных.")

        # Разбиваем переменные для строк и столбцов
        if num_vars <= 4:
            group_1_vars = self.variables[:num_vars // 2]  # Переменные для строк
            group_2_vars = self.variables[num_vars // 2:]  # Переменные для столбцов
        else:
            group_1_vars = self.variables[:2]  # Для строк - первые 2 переменные
            group_2_vars = self.variables[2:]  # Для столбцов - оставшиеся 3 переменные

        # Генерируем заголовки строк и столбцов
        row_headers = self._generate_gray_code(len(group_1_vars))  # Последовательности для строк
        col_headers = self._generate_gray_code(len(group_2_vars))  # Последовательности для столбцов

        # Карта Карно для заполнения
        karnaugh_map = [
            [None for _ in col_headers]
            for _ in row_headers
        ]

        # Заполняем карту Карно
        for row_header in range(len(row_headers)):
            for col_header in range(len(col_headers)):
                # Объединяем значения строки и столбца
                combination = row_headers[row_header] + col_headers[col_header]
                # Ищем результат из таблицы истинности
                for entry in simplified_table:
                    if entry[:num_vars] == combination:
                        karnaugh_map[row_header][col_header] = entry[-1]

        return {
            "rows": row_headers,
            "columns": col_headers,
            "map": karnaugh_map
        }

    def display_karnaugh_map(self):
        """
        Красиво выводит таблицу Карно с указанием расположения переменных.
        Поддерживает до 5 переменных.
        """
        kmap = self.generate_karnaugh_map()

        rows = kmap["rows"]
        columns = kmap["columns"]
        karnaugh_map = kmap["map"]

        # Получаем переменные, распределенные по строкам и столбцам
        num_vars = len(self.variables)
        if num_vars <= 4:
            row_vars = self.variables[:num_vars // 2]  # Переменные для строк
            col_vars = self.variables[num_vars // 2:]  # Переменные для столбцов
        else:
            row_vars = self.variables[:2]  # Первые 2 переменные для строк
            col_vars = self.variables[2:]  # Остальные 3 переменные для столбцов

        # Печатаем заголовки переменных
        print(f"Строки ({','.join(row_vars)})")
        print(f"Столбцы ({','.join(col_vars)})")
        print()

        # Определяем ширину каждой ячейки для выравнивания
        cell_width = max(
            len("".join(map(str, col))) for col in (columns + rows)
        ) + 2  # Ширина для заголовков и содержимого

        # Построение заголовка таблицы
        col_header = " " * (len(row_vars) + 3)  # Отступ для строк
        col_header += " | ".join(f"{''.join(map(str, col)):^{cell_width}}" for col in columns)
        print(col_header)
        print(" " * (len(row_vars) + 3) + "-" * (len(col_header) - (len(row_vars) + 3)))

        # Построение строк таблицы Карно
        for row, values in zip(rows, karnaugh_map):
            row_header = "".join(map(str, row)).ljust(3)  # Заголовок строки
            row_values = " | ".join(f"{str(v) if v is not None else '-':^{cell_width}}" for v in values)
            print(f"{row_header}{row_values}")

    @staticmethod
    def _generate_gray_code(num_bits):
        """
        Генерирует последовательность Грея для заданного количества бит.
        """
        if num_bits == 0:
            return [[]]
        smaller = KarnaughMinimizer._generate_gray_code(num_bits - 1)
        return [[0] + code for code in smaller] + [[1] + code for code in reversed(smaller)]



    def minimize_sdnf(self):
        """
        Минимизирует СДНФ непосредственно на основе карты Карно, с учётом групп от больших к малым.
        """
        kmap = self.generate_karnaugh_map()
        rows = kmap["rows"]
        columns = kmap["columns"]
        karnaugh_map = kmap["map"]

        minimized_terms = []  # Результирующий список минимальных термов

        # Остаток карты Карно (ячейки, которые нужно покрыть)
        uncovered_cells = {
            (row, col)
            for row in range(len(rows))
            for col in range(len(columns))
            if karnaugh_map[row][col] == 1
        }

        # Ищем группы по убыванию размера
        for size in [4, 2, 1]:  # Размеры групп (максимальный по поддержке: 2x2, 1x2, 1x1)
            for row_idx in range(len(rows)):
                for col_idx in range(len(columns)):
                    if (row_idx, col_idx) not in uncovered_cells:
                        continue

                    # Ищем группу данного размера
                    group = self._find_group_d(row_idx, col_idx, size, karnaugh_map, rows, columns, uncovered_cells)
                    if group:
                        # Формируем логическое выражение для группы
                        term = self._group_to_expression_d(group, rows, columns)
                        minimized_terms.append(term)

                        # Убираем покрытые клетки из остатка
                        uncovered_cells -= group

        # Конвертируем минимизированные термы в финальное строковое представление
        return " | ".join(
            f"({' & '.join(filter(None, term))})" for term in minimized_terms
        )

    def minimize_sknf(self):
        """
        Минимизирует СКНФ непосредственно на основе карты Карно, с учётом групп от больших к малым.
        """
        kmap = self.generate_karnaugh_map()
        rows = kmap["rows"]
        columns = kmap["columns"]
        karnaugh_map = kmap["map"]

        minimized_terms = []  # Результирующий список минимальных термов

        # Остаток карты Карно (ячейки, которые нужно покрыть)
        uncovered_cells = {
            (row, col)
            for row in range(len(rows))
            for col in range(len(columns))
            if karnaugh_map[row][col] == 0  # РАБОТАЕМ С НУЛЯМИ
        }

        # Ищем группы по убыванию размера
        for size in [4, 2, 1]:  # Размеры групп (максимальный по поддержке: 2x2, 1x2, 1x1)
            for row_idx in range(len(rows)):
                for col_idx in range(len(columns)):
                    if (row_idx, col_idx) not in uncovered_cells:
                        continue

                    # Ищем группу данного размера
                    group = self._find_group_k(row_idx, col_idx, size, karnaugh_map, rows, columns, uncovered_cells)
                    if group:
                        # Формируем логическое выражение для группы
                        term = self._group_to_expression_k(group, rows, columns, sknf=True)  # Добавляем флаг для СКНФ
                        minimized_terms.append(term)

                        # Убираем покрытые клетки из остатка
                        uncovered_cells -= group

        return " & ".join(
            f"({' | '.join(filter(None, term))})" for term in minimized_terms
        )


    def _generate_term(self, row_values, col_values):
        """
        Генерируем терм для конкретной ячейки Карты Карно.
        """
        term = []
        combined = row_values + col_values  # Фиксируем значения строки и столбца
        for idx, value in enumerate(combined):
            if value == 1:
                term.append(self.variables[idx])
            elif value == 0:
                term.append(f"!{self.variables[idx]}")
        return term

    def _perform_grouping(self, terms):
        """
        Группирует термы для минимизации.
        """
        grouped = []

        for term in terms:
            # Пытаемся объединить текущий терм с уже существующими
            for i, existing_term in enumerate(grouped):
                if self._can_be_grouped(term, existing_term):
                    grouped[i] = self._combine_terms(term, existing_term)
                    break
            else:
                grouped.append(term)

        return grouped

    def _can_be_grouped(self, term1, term2):
        """
        Проверяет, можно ли объединить два терма.
        """
        differences = 0
        for t1, t2 in zip(term1, term2):
            if t1 != t2:
                differences += 1
            if differences > 1:
                return False
        return True

    def _combine_terms(self, term1, term2):
        """
        Объединяет два терма, заменяя различия на None.
        """
        return [
            t1 if t1 == t2 else None
            for t1, t2 in zip(term1, term2)
        ]

    def _minimize_cell(self, row, col, kmap, rows, columns, used_cells):
        """
        Оптимизирует выражение для указанной ячейки.
        """
        num_rows = len(kmap)
        num_cols = len(kmap[0])
        group = set()
        group.add((row, col))
        used_cells.add((row, col))

        # Формируем термы для минимизации
        row_values = rows[row]
        col_values = columns[col]
        fixed_values = row_values + col_values

        # Проверяем соседние клетки для объединения (по вертикали, горизонтали)
        for r, c in [(row, (col + 1) % num_cols), ((row + 1) % num_rows, col)]:
            if kmap[r][c] == 1 and (r, c) not in used_cells:
                group.add((r, c))
                used_cells.add((r, c))
                combined_values = rows[r] + columns[c]
                fixed_values = [
                    fv if fv == cv else None
                    for fv, cv in zip(fixed_values, combined_values)
                ]

        # Формируем конечный терм
        term = []
        for i, value in enumerate(fixed_values):
            if value is not None:
                term.append(self.variables[i] if value == 1 else f"!{self.variables[i]}")

        return term

    def _find_group_d(self, row, col, size, kmap, rows, columns, used_cells):
        """
        Ищет группу указанного размера size, начиная с позиции (row, col),
        с учётом циклической смежности строк и столбцов.
        """
        num_rows = len(rows)
        num_cols = len(columns)

        # Группа из 4 ячеек (2x2 блок)
        if size == 4:
            group = {
                (row % num_rows, col % num_cols),
                (row % num_rows, (col + 1) % num_cols),
                ((row + 1) % num_rows, col % num_cols),
                ((row + 1) % num_rows, (col + 1) % num_cols),
            }
            if all(kmap[r][c] == 1 for r, c in group):
                return group

        # Горизонтальная группа из 2 ячеек
        if size == 2:
            group_horizontal = {
                (row % num_rows, col % num_cols),
                (row % num_rows, (col + 1) % num_cols),
            }
            if all(kmap[r][c] == 1 for r, c in group_horizontal):
                return group_horizontal

            # Вертикальная группа из 2 ячеек
            group_vertical = {
                (row % num_rows, col % num_cols),
                ((row + 1) % num_rows, col % num_cols),
            }
            if all(kmap[r][c] == 1 for r, c in group_vertical):
                return group_vertical

        # Одиночная ячейка (размер 1)
        if size == 1:
            group_single = {(row % num_rows, col % num_cols)}
            if kmap[row % num_rows][col % num_cols] == 1:
                return group_single

        return None

    def _find_group_k(self, row, col, size, kmap, rows, columns, used_cells):
        """
        Ищет группу указанного размера size, начиная с позиции (row, col),
        с учётом циклической смежности строк и столбцов.
        """
        num_rows = len(rows)
        num_cols = len(columns)

        # Группа из 4 ячеек (2x2 блок)
        if size == 4:
            group = {
                (row % num_rows, col % num_cols),
                (row % num_rows, (col + 1) % num_cols),
                ((row + 1) % num_rows, col % num_cols),
                ((row + 1) % num_rows, (col + 1) % num_cols),
            }
            if all(kmap[r][c] == 0 for r, c in group):  # Ищем нули
                return group

        # Горизонтальная группа из 2 ячеек
        if size == 2:
            group_horizontal = {
                (row % num_rows, col % num_cols),
                (row % num_rows, (col + 1) % num_cols),
            }
            if all(kmap[r][c] == 0 for r, c in group_horizontal):
                return group_horizontal

            # Вертикальная группа из 2 ячеек
            group_vertical = {
                (row % num_rows, col % num_cols),
                ((row + 1) % num_rows, col % num_cols),
            }
            if all(kmap[r][c] == 0 for r, c in group_vertical):
                return group_vertical

        # Одиночная ячейка (размер 1)
        if size == 1:
            group_single = {(row % num_rows, col % num_cols)}
            if kmap[row % num_rows][col % num_cols] == 0:  # Проверяем 0
                return group_single

        return None

    def _group_to_expression_d(self, group, rows, columns):
        """
        Преобразует группу ячеек в логическое выражение, оставляя только фиксированные переменные.
        """
        num_vars = len(self.variables)
        fixed_values = [None] * num_vars  # Массив фиксированных значений для каждой переменной

        # Анализ значений в группе
        for row, col in group:
            row_values = rows[row]
            col_values = columns[col]
            combined = row_values + col_values  # Комбинируем значения строки и столбца

            # Сравниваем и фиксируем значения для переменных
            for i, value in enumerate(combined):
                if fixed_values[i] is None:
                    fixed_values[i] = value
                elif fixed_values[i] != value:
                    print(f"Переменная {self.variables[i]} сброшена (меняется в группе)")  # Отладка
                    fixed_values[i] = None  # Значение меняется — удаляем

        # Генерация терма
        term = []
        for i, var in enumerate(self.variables):
            if fixed_values[i] is not None:  # Только неизменные переменные включаем в терм
                if fixed_values[i] == 1:
                    term.append(var)
                else:
                    term.append(f"!{var}")
        print(f"Сформирован терм: {term}")  # Отладка
        return term

    def _group_to_expression_k(self, group, rows, columns, sknf=False):
        """
        Преобразует группу ячеек в логическое выражение, оставляя только фиксированные переменные.
        Поддерживает СКНФ и СДНФ.
        """
        num_vars = len(self.variables)
        fixed_values = [None] * num_vars  # Массив фиксированных значений для каждой переменной

        # Анализ значений в группе
        for row, col in group:
            row_values = rows[row]
            col_values = columns[col]
            combined = row_values + col_values  # Комбинируем значения строки и столбца

            # Сравниваем и фиксируем значения для переменных
            for i, value in enumerate(combined):
                if fixed_values[i] is None:
                    fixed_values[i] = value
                elif fixed_values[i] != value:
                    fixed_values[i] = None  # Значение меняется — удаляем

        # Генерация терма
        term = []
        for i, var in enumerate(self.variables):
            if fixed_values[i] is not None:  # Только неизменные переменные включаем в терм
                if sknf:  # Для СКНФ меняем логику
                    if fixed_values[i] == 0:
                        term.append(var)  # Если 0, добавляем переменную без отрицания
                    else:
                        term.append(f"!{var}")  # Если 1, добавляем с отрицанием
                else:  # Логика для СДНФ
                    if fixed_values[i] == 1:
                        term.append(var)
                    else:
                        term.append(f"!{var}")

        return term