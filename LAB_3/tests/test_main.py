import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import logical_processing.main as main_module


class TestMainFunction(unittest.TestCase):
    def test_main_correct_expression(self):
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

        for part in expected_output_parts:
            self.assertIn(part, output)

    def test_main_invalid_expression(self):
        user_input = "invalid_expression"
        expected_error_message = "Ошибка:"

        with patch("builtins.input", return_value=user_input), patch("sys.stdout",
                                                                     new_callable=StringIO) as mock_stdout:
            main_module.main()
            output = mock_stdout.getvalue()

        self.assertIn(expected_error_message, output)

    def test_main_sdnf_and_sknf_methods(self):
        user_input = "a & b | !c"
        expected_output_parts = [
            "============================================ МЕТОД 3 ============================================",
            "============================================ СДНФ ============================================",
            "============================================ СKНФ ============================================",
            "Минимизированная СДНФ:",
            "Минимизированная СКНФ:",
        ]

        with patch("builtins.input", return_value=user_input), patch("sys.stdout",
                                                                     new_callable=StringIO) as mock_stdout:
            main_module.main()
            output = mock_stdout.getvalue()

        for part in expected_output_parts:
            self.assertIn(part, output)

    def test_main_methods_logic(self):
        user_input = "(a | b | !c) & (!a | b | c)"

        with patch("builtins.input", return_value=user_input), patch("sys.stdout",
                                                                     new_callable=StringIO) as mock_stdout:
            main_module.main()
            output = mock_stdout.getvalue()

        self.assertIn("Минимизированная СДНФ:", output)
        self.assertIn("Минимизированная СКНФ:", output)

    def test_main_exception_handling(self):
        user_input = "(a & b & (c | d)"

        with patch("builtins.input", return_value=user_input), patch("sys.stdout",
                                                                     new_callable=StringIO) as mock_stdout:
            main_module.main()
            output = mock_stdout.getvalue()

        self.assertIn("Ошибка:", output)


if __name__ == "__main__":
    unittest.main()
