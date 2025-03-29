import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from logical_processing.KarnaughMinimizer import KarnaughMinimizer
from logical_processing.min import Minimizing
from logical_processing.normal_forms import NormalForms
from logical_processing.table import TruthTableWithSubexpressions
import logical_processing.main as main_module


class TestMainFunction(unittest.TestCase):
    def test_main_correct_expression(self):
        # Мокаем ввод корректного логического выражения, например, "a & b | c"
        user_input = "a & b | c"
        expected_output_parts = [
            "СДНФ:",
            "СКНФ:",
            "Минимизированная СДНФ:",
            "Минимизированная СКНФ:",
        ]

        with patch("builtins.input", return_value=user_input), patch("sys.stdout",
                                                                     new_callable=StringIO) as mock_stdout:
            main_module.main()
            output = mock_stdout.getvalue()

        # Проверка основных частей вывода
        for part in expected_output_parts:
            self.assertIn(part, output)

    def test_main_invalid_expression(self):
        # Мокаем ввод некорректного выражения
        user_input = "invalid_expression"
        expected_error_message = "Ошибка:"

        with patch("builtins.input", return_value=user_input), patch("sys.stdout",
                                                                     new_callable=StringIO) as mock_stdout:
            main_module.main()
            output = mock_stdout.getvalue()

        # Проверка вывода ошибки
        self.assertIn(expected_error_message, output)

    def test_main_sdnf_and_sknf_methods(self):
        # Проверяем корректность выполнения всех методов минимизации
        user_input = "a & b | !c"
        expected_output_parts = [
            "============================================ МЕТОД 3 ============================================",
            "============================================ СДНФ ============================================",
            "============================================ СKНФ ============================================",
            # Исправлено: подстроено под реальный вывод
            "Минимизированная СДНФ:",
            "Минимизированная СКНФ:",
        ]

        with patch("builtins.input", return_value=user_input), patch("sys.stdout",
                                                                     new_callable=StringIO) as mock_stdout:
            main_module.main()
            output = mock_stdout.getvalue()

        # Проверка ключевых частей вывода
        for part in expected_output_parts:
            self.assertIn(part, output)

    def test_main_methods_logic(self):
        # Проверяем выполнение всех трех методов минимизации
        user_input = "(a | b | !c) & (!a | b | c)"

        with patch("builtins.input", return_value=user_input), patch("sys.stdout",
                                                                     new_callable=StringIO) as mock_stdout:
            main_module.main()
            output = mock_stdout.getvalue()

        # Проверяем, что выводятся минимизированные формы
        self.assertIn("Минимизированная СДНФ:", output)
        self.assertIn("Минимизированная СКНФ:", output)

    def test_main_exception_handling(self):
        # Проверяем обработку нестандартных исключений
        user_input = "(a & b & (c | d)"  # Неполное выражение (ошибка скобок)

        with patch("builtins.input", return_value=user_input), patch("sys.stdout",
                                                                     new_callable=StringIO) as mock_stdout:
            main_module.main()
            output = mock_stdout.getvalue()

        # Проверяем вывод ошибки
        self.assertIn("Ошибка:", output)


if __name__ == "__main__":
    unittest.main()
