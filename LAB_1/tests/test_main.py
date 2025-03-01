import unittest
from unittest.mock import patch
from main import Main


class TestMain(unittest.TestCase):

    @patch('builtins.input', side_effect=['10'])
    @patch('builtins.print')
    def test_exit_program(self, mock_print, mock_input):
        program = Main()
        program.run()
        mock_print.assert_any_call("Выход из программы.")

    @patch('builtins.input', side_effect=['1', '5', '3', '10'])
    @patch('binary_calculator.converter.Converter.display_number_binary')
    @patch('builtins.print')
    def test_convert_to_binary(self, mock_print, mock_display_binary, mock_input):
        program = Main()
        program.run()
        mock_display_binary.assert_called_once()
        mock_print.assert_any_call("Выберите операцию: ")

    @patch('builtins.input', side_effect=['9', '2.5', '3.5', '10'])
    @patch('builtins.print')
    def test_ieee754_addition(self, mock_print, mock_input):
        program = Main()
        program.run()
        mock_print.assert_any_call("Сложение чисел с плавающей точкой StandartIEEE754:")

    @patch('builtins.input', side_effect=['5', '3', '5', '8', '10'])
    @patch('binary_calculator.add_sub.AddSub.display_add_additional')
    @patch('builtins.print')
    def test_additional_code_sum(self, mock_print, mock_display_additional, mock_input):
        program = Main()
        program.run()
        mock_display_additional.assert_called_once()
        mock_print.assert_any_call("Сложение:")

    @patch('builtins.input', side_effect=['6', '10', '5', '8', '10'])
    @patch('binary_calculator.add_sub.AddSub.display_add_additional')
    @patch('builtins.print')
    def test_additional_code_subtraction(self, mock_print, mock_display_additional, mock_input):
        program = Main()
        program.run()
        mock_display_additional.assert_called_once()
        mock_print.assert_any_call("Вычитание в дополнительном коде:")

    @patch('builtins.input', side_effect=['7', '4', '3', '8', '10'])
    @patch('binary_calculator.operations.Operations.display_mult_direct')
    @patch('binary_calculator.operations.Operations.multiply_direct')
    @patch('binary_calculator.operations.Operations.display_number_info')
    @patch('builtins.print')
    def test_multiply_direct_code(self, mock_print, mock_display_info, mock_multiply, mock_display_mult, mock_input):
        mock_multiply.return_value = (12, '1100')

        program = Main()
        program.run()

    @patch('builtins.input', side_effect=['8', '15', '3', '8', '10'])
    @patch('binary_calculator.operations.Operations.binary_divide')
    @patch('binary_calculator.operations.Operations.display_number_info')
    @patch('builtins.print')
    def test_binary_divide(self, mock_print, mock_display_info, mock_divide, mock_input):
        mock_divide.return_value = (5.0, '101')

        program = Main()
        program.run()



if __name__ == '__main__':
    unittest.main()
