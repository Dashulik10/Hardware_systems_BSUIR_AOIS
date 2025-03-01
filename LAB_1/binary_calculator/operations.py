from binary_calculator.converter import *

class Operations:
    DEFAULT_BITS = 8

    DEFAULT_PRECISION = 5
    DIRECT_CODE_TAG = "Прямой код"


    def __init__(self, number_1, number_2=None, bits=DEFAULT_BITS):
        self.number_1 = number_1
        self.number_2 = number_2
        self.bits = bits

    # Умножение прямой код
    def multiply_direct(self):
        number_1_direct = self.direct_code(self.number_1)
        number_2_direct = self.direct_code(self.number_2)

        sign_1 = int(number_1_direct[0])
        sign_2 = int(number_2_direct[0])

        number_1_abs = int(number_1_direct[1:], 2)
        number_2_abs = int(number_2_direct[1:], 2)

        result_abs = number_1_abs * number_2_abs

        result_sign = "0" if sign_1 == sign_2 else "1"

        max_value = (1 << (self.bits - 1)) - 1
        if result_abs > max_value:
            OVERFLOW_ERROR = "Переполнение: результат {result_abs} не помещается в {self.bits} бит."
            raise OverflowError(OVERFLOW_ERROR)

        result_binary = bin(result_abs)[2:].zfill(self.bits - 1)
        result_binary = result_sign + result_binary

        result_decimal = -result_abs if result_sign == "1" else result_abs

        return result_decimal, result_binary

    # Деление прямой код
    def binary_divide(self, precision=DEFAULT_PRECISION):
        if self.number_2 == 0:
            DIVISION_BY_ZERO_ERROR = "Деление на ноль невозможно!"
            raise ZeroDivisionError(DIVISION_BY_ZERO_ERROR)

        def direct_code(n):
            if n >= 0:
                return f"0{n:0{self.bits - 1}b}"
            else:
                return f"1{(-n):0{self.bits - 1}b}"

        number_1_direct = direct_code(self.number_1)
        number_2_direct = direct_code(self.number_2)

        sign_1 = int(number_1_direct[0])
        sign_2 = int(number_2_direct[0])
        result_sign = "0" if sign_1 == sign_2 else "1"

        dividend = int(number_1_direct[1:], 2) # делимое
        divisor = int(number_2_direct[1:], 2) # делитель

        shift_count = 0
        while divisor < dividend:
            divisor <<= 1
            shift_count += 1

        quotient = ""

        for _ in range(shift_count + 1):
            if dividend >= divisor:
                quotient += "1"
                dividend -= divisor
            else:
                quotient += "0"
            divisor >>= 1

        BINARY_POINT = "."
        quotient += BINARY_POINT

        for _ in range(precision):
            dividend <<= 1
            if dividend >= int(number_2_direct[1:], 2):
                quotient += "1"
                dividend -= int(number_2_direct[1:], 2)
            else:
                quotient += "0"

        integer_part, fractional_part = quotient.split(".")
        decimal_value = int(integer_part, 2) + sum(
            int(bit) * (2 ** -(i + 1)) for i, bit in enumerate(fractional_part)
        )

        if result_sign == "1":
            decimal_value = -decimal_value

        res_binary = result_sign + integer_part + "." + fractional_part

        return decimal_value, res_binary

    def display_mult_direct(self, decimal_value, res_binary, bits=DEFAULT_BITS):
        converter = Converter(decimal_value, bits)
        print(f"Результат: {decimal_value}")
        print(f"Прямой код: {res_binary}")
        print(f"Обратный код: [{converter.reverse_code()}]")
        print(f"Дополнительный код: [{converter.additional_code()}]")

    def display_number_info(self, number, bits=DEFAULT_BITS):

        converter = Converter(number, self.bits)
        print(f"Число введено: {number}")
        print(f"Прямой код: [{converter.direct_code()}]")
        print(f"Обратный код: [{converter.reverse_code()}]")
        print(f"Дополнительный код: [{converter.additional_code()}]\n")

    def direct_code(self, number):
        if number >= 0:
            bin_number = bin(number)[2:].zfill(self.bits - 1)
            return "0" + bin_number
        else:
            bin_number = bin(abs(number))[2:].zfill(self.bits - 1)
            return "1" + bin_number
