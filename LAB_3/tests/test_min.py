import unittest
from unittest.mock import MagicMock
from logical_processing.expression_validator import ExpressionValidator
from logical_processing.min import Minimizing
from logical_processing.table import TruthTableWithSubexpressions
from logical_processing.KarnaughMinimizer import KarnaughMinimizer


class TestKarnaughMinimizer(unittest.TestCase):
    def setUp(self):
        self.expression = "a & b | !a & c"
        self.minimizer = KarnaughMinimizer(self.expression)

        # Моки для зависимых компонентов
        self.mock_truth_table_generator = MagicMock()
        self.minimizer.truth_table_generator = self.mock_truth_table_generator
        ExpressionValidator.VARIABLES = {"a", "b", "c", "d"}  # Переменные для работы ExpressionValidator

    def test_generate_simplified_table(self):
        # Заготовка данных для таблицы истинности
        self.mock_truth_table_generator.generate_table.return_value = [
            ({"a": 0, "b": 0, "c": 0}, None, 0),
            ({"a": 0, "b": 0, "c": 1}, None, 1),
            ({"a": 0, "b": 1, "c": 0}, None, 1),
            ({"a": 1, "b": 0, "c": 0}, None, 1),
        ]

        # Ожидаемый результат
        expected_table = [
            [0, 0, 0, 0],
            [0, 0, 1, 1],
            [0, 1, 0, 1],
            [1, 0, 0, 1]
        ]

        simplified_table = self.minimizer.generate_simplified_table()
        self.assertEqual(simplified_table, expected_table)

    def test_generate_karnaugh_map(self):
        # Заготовка данных для таблицы истинности
        self.mock_truth_table_generator.generate_table.return_value = [
            ({"a": 0, "b": 0, "c": 0}, None, 0),
            ({"a": 0, "b": 0, "c": 1}, None, 1),
            ({"a": 1, "b": 1, "c": 0}, None, 1),
            ({"a": 1, "b": 1, "c": 1}, None, 0),
        ]

        # Ожидаемый результат генерации карты Карно
        expected_karnaugh_map = {
            "rows": [[0], [1]],
            "columns": [[0, 0], [0, 1], [1, 1], [1, 0]],
            "map": [
                [0, 1, None, None],
                [None, None, 0, 1]
            ]
        }

        kmap = self.minimizer.generate_karnaugh_map()
        self.assertEqual(kmap, expected_karnaugh_map)

    def test_find_group(self):
        # Готовим данные для карты Карно
        kmap = [[1, 1], [1, 1]]  # Полностью заполненная карта (2x2)
        rows = [[0], [1]]
        columns = [[0], [1]]
        used_cells = set()  # Передаём пустое множество

        # Ищем группу из четырёх ячеек
        group = self.minimizer._find_group_d(0, 0, size=4, kmap=kmap, rows=rows, columns=columns, used_cells=used_cells)
        expected_group = {(0, 0), (0, 1), (1, 0), (1, 1)}
        self.assertEqual(group, expected_group)

    def test_minimize_sdnf(self):
        # Мокаем метод для генерации Карно
        self.minimizer.generate_karnaugh_map = MagicMock(return_value={
            "rows": [[0], [1]],
            "columns": [[0, 0], [0, 1], [1, 1], [1, 0]],
            "map": [
                [0, 1, 0, 1],
                [1, 1, 0, 1]
            ]
        })

        # Проверяем минимизацию
        result = self.minimizer.minimize_sdnf()
        expected_result = "(!b & c) | (b & !c) | (a & !b)"
        self.assertEqual(result, expected_result)

    def test_group_to_expression(self):
        # Тест преобразования группы в выражение
        group = {(0, 0), (0, 1), (1, 0), (1, 1)}
        rows = [[0], [1]]
        columns = [[0, 0], [0, 1]]
        result = self.minimizer._group_to_expression_d(group, rows, columns)
        expected_result = ['!b']  # Все переменные изменяются — пустой терм
        self.assertEqual(result, expected_result)

        # Тест с фиксированными переменными
        group = {(0, 0), (0, 1)}
        result = self.minimizer._group_to_expression_d(group, rows, columns)
        expected_result = ['!a', '!b']  # Переменная "a" фиксирована
        self.assertEqual(result, expected_result)

    def test_invalid_karnaugh_map(self):
        # Генерация карты с неподдерживаемым количеством переменных
        self.minimizer.variables = ["a"]  # Только одна переменная
        with self.assertRaises(ValueError):
            self.minimizer.generate_karnaugh_map()

        self.minimizer.variables = ["a", "b", "c", "d", "e", "f"]  # Для шести переменных
        with self.assertRaises(ValueError):
            self.minimizer.generate_karnaugh_map()

class TestMinimizing(unittest.TestCase):

    def setUp(self):
        self.variables = ['a', 'b', 'c']
        self.expression_sdnf = "(a & b & c) | (!a & b & !c) | (a & !b & c)"
        self.expression_sknf = "(a | b | !c) & (!a | b | c) & (a | !b | c)"
        self.terms_sdnf = [[1, 1, 1], [0, 1, 0], [1, 0, 1]]
        self.terms_sknf = [[1, 1, 0], [0, 1, 1], [1, 0, 1]]

        # Инициализация минимайзера
        self.minimizer = KarnaughMinimizer(self.expression_sknf)

        # Мок для генератора таблиц
        self.mock_truth_table_generator = MagicMock()
        self.minimizer.truth_table_generator = self.mock_truth_table_generator

    def test_terms_sdnf(self):
        # Тест преобразования СДНФ в списки термов
        result = Minimizing.terms_sdnf(self.expression_sdnf)
        self.assertEqual(result, self.terms_sdnf)

    def test_term_to_expression_sdnf(self):
        # Тест преобразования терма в строковое представление
        term = [1, 0, 1]  # a & !b & c
        result = Minimizing.term_to_expression_sdnf(term, self.variables)
        self.assertEqual(result, "a & !b & c")

    def test_terms_sknf(self):
        # Тест преобразования СКНФ в списки термов
        result = Minimizing.terms_sknf(self.expression_sknf)
        self.assertEqual(result, self.terms_sknf)

    def test_term_to_expression_sknf(self):
        # Тест преобразования терма в строковое представление для СКНФ
        term = [1, 0, 1]  # a | !b | c
        result = Minimizing.term_to_expression_sknf(term, self.variables)
        self.assertEqual(result, "a | !b | c")

    def test_compare_terms_sdnf(self):
        # Тест сравнения термов (шаг 1 в минимизации)
        terms = [[1, 1, 1], [1, 1, 0], [1, 0, 1], [0, 0, 1]]
        result = Minimizing.compare_terms_sdnf(terms, self.variables)
        expected = [[1, 1, 'X'], [1, 'X', 1], ['X', 0, 1]]
        self.assertEqual(result, expected)

    def test_minimize_sdnf(self):
        # Тест минимизации СДНФ
        result = Minimizing.minimize_sdnf(self.expression_sdnf, self.variables)
        expected = [[1, 'X', 1], [0, 1, 0]]
        self.assertEqual(result, expected)

    def test_minimize_sdnf_second(self):
        # Тест минимизации СДНФ с выводом таблицы
        result = Minimizing.minimize_sdnf_second(self.expression_sdnf, self.variables)
        expected = [[1, 'X', 1], [0, 1, 0]]
        self.assertEqual(result, expected)

    def test_minimize_sknf_second(self):
        # Тест минимизации СКНФ с выводом таблицы
        result = Minimizing.minimize_sknf_second(self.expression_sknf, self.variables)
        expected = [[1, 1, 0], [0, 1, 1], [1, 0, 1]]
        self.assertEqual(result, expected)



    def test_minimize_sknf(self):
        # Мокаем метод для генерации Карно
        self.minimizer.generate_karnaugh_map = MagicMock(return_value={
            "rows": [[0], [1]],
            "columns": [[0, 0], [0, 1], [1, 1], [1, 0]],
            "map": [
                [1, 0, 0, 1],
                [0, 1, 1, 0]
            ]
        })

        # Проверяем минимизацию СКНФ
        result = self.minimizer.minimize_sknf()
        expected_result = "(a | !c) & (!a | c)"  # Ожидаемый результат
        self.assertEqual(result, expected_result)

    def test_find_group_k(self):
        # Готовим данные для карты Карно
        kmap = [[0, 0], [0, 1]]  # Карта с нулями
        rows = [[0], [1]]
        columns = [[0], [1]]
        used_cells = set()  # Передаём пустое множество

        # Ищем группу из двух ячеек
        group = self.minimizer._find_group_k(0, 0, size=2, kmap=kmap, rows=rows, columns=columns, used_cells=used_cells)
        expected_group = {(0, 0), (0, 1)}  # Группа двух смежных нулей
        self.assertEqual(group, expected_group)

    def test_group_to_expression_k(self):
        # Группа нулевых ячеек
        group = {(0, 0), (0, 1)}
        rows = [[0], [1]]
        columns = [[0, 0], [0, 1]]
        result = self.minimizer._group_to_expression_k(group, rows, columns, sknf=True)
        expected_result = ["a", "b"]  # Ожидаем, что переменные формируют дизъюнкцию для СКНФ
        self.assertEqual(result, expected_result)

        # Тест с другой группой нулей
        group = {(1, 0), (1, 1)}
        result = self.minimizer._group_to_expression_k(group, rows, columns, sknf=True)
        expected_result = ["!a", "b"]  # Ожидаемая дизъюнкция с отрицаниями
        self.assertEqual(result, expected_result)

    def test_full_minimize_sknf_process(self):
        # Заготовка данных для таблицы истинности
        self.mock_truth_table_generator.generate_table.return_value = [
            ({"a": 0, "b": 0, "c": 0}, None, 1),  # 1 -> подходит для СКНФ
            ({"a": 0, "b": 0, "c": 1}, None, 0),  # 0 -> участвует в минимизации
            ({"a": 1, "b": 1, "c": 0}, None, 0),  # 0 -> участвует в минимизации
            ({"a": 1, "b": 1, "c": 1}, None, 1),  # 1 -> не участвует
        ]

        # Ожидаемый СКНФ
        expected_result = "(a | b | !c) & (!a | !b | c)"  # Пример СКНФ

        # Генерация карты Карно
        self.minimizer.generate_table()
        result = self.minimizer.minimize_sknf()
        self.assertEqual(result, expected_result)
class TestMinimizeSKNF(unittest.TestCase):
    def setUp(self):
        self.variables = ["a", "b", "c"]

    def test_minimize_sknf_simple(self):
        # Тест минимизации простого выражения
        expression = "(a | b | !c) & (!a | !b | c)"
        result = Minimizing.minimize_sknf(expression, self.variables)

        # Ожидаемый результат: уже минимальное выражение
        expected = [[1, 1, 0], [0, 0, 1]]
        self.assertEqual(result, expected)


    def test_minimize_sknf_from_terms(self):
        # Тест минимизации, когда вход - список термов
        terms = [[1, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1]]
        result = Minimizing.minimize_sknf(terms, self.variables)

        # Ожидаемый результат после минимизации
        expected = [['X', 0, 1], [0, 'X', 1], [1, 1, 0]]
        self.assertEqual(result, expected)

    def test_minimize_sknf_with_redundant_terms(self):
        # Тест с избыточными импликантами, которые должны быть удалены
        expression = "(a | b | !c) & (!a | b | c) & (a | !b | c)"
        result = Minimizing.minimize_sknf(expression, self.variables)

        # Убираются избыточные импликанты
        expected = [[1, 1, 0], [0, 1, 1], [1, 0, 1]]
        self.assertEqual(result, expected)

    def test_minimize_sknf_no_reduction(self):
        # Тест на случай, когда нет возможности минимизации
        expression = "(a | b | !c) & (a | b | c)"
        result = Minimizing.minimize_sknf(expression, self.variables)

        # Уже минимальное выражение
        expected = [[1, 1, 'X']]
        self.assertEqual(result, expected)

    def test_minimize_sknf_long_expression(self):
        # Тест на длинное выражение
        expression = "(a | b | c) & (!a | b | c) & (a | !b | c) & (!a | !b | !c)"
        result = Minimizing.minimize_sknf(expression, self.variables)

        # После минимизации ожидается удаление избыточных термов
        expected = [['X', 1, 1], [1, 'X', 1], [0, 0, 0]]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()

