from binary_calculator.converter import *

class AddSub:
    DEFAULT_BITS = 8
    ERROR_OVERFLOW_MESSAGE = "Переполнение при сложении в дополнительном коде!"
    NEGATIVE_SIGN_ADJUSTMENT = 1
    BINARY_BASE = 2

    def __init__(self, number_1, number_2=None, bits=DEFAULT_BITS):
        self.number_1 = number_1
        self.number_2 = number_2
        self.bits = bits


    def add_additional(self):
        number_1_additional = AddSub.additional_code(self.number_1, self.bits)
        number_2_additional = AddSub.additional_code(self.number_2, self.bits)

        init_carry = 0
        result_additional = ""

        for i in range(self.bits - 1, -1, -1):
            bit1 = int(number_1_additional[i])
            bit2 = int(number_2_additional[i])

            sum_bit = bit1 + bit2 + init_carry
            result_additional = str(sum_bit % 2) + result_additional
            init_carry = sum_bit // 2

        sign_bit_1 = int(number_1_additional[0])
        sign_bit_2 = int(number_2_additional[0])
        sign_bit_res = int(result_additional[0])

        if (sign_bit_1 == sign_bit_2) and (sign_bit_res != sign_bit_1):
            raise OverflowError("Переполнение при сложении в дополнительном коде!")

        if result_additional[0] == "1":
            result_decimal = int(result_additional, AddSub.BINARY_BASE) - (AddSub.NEGATIVE_SIGN_ADJUSTMENT << self.bits)
        else:
            result_decimal = int(result_additional, AddSub.BINARY_BASE)

        return result_decimal, result_additional

    def subtract_additional(self):
        self.number_2 = -self.number_2
        return self.add_additional()

    def display_add_additional(self, result_decimal, result_additional):

        print(f"Результат: {result_decimal}")
        converter_result = Converter(result_decimal, self.bits)
        print(f"Прямой код: [{converter_result.direct_code()}]")
        print(f"Обратный код: [{converter_result.reverse_code()}]")
        print(f"Дополнительный код: {result_additional}\n")

    def display_number_info(self, number):

        converter = Converter(number, self.bits)
        print(f"Число введено: {number}")
        print(f"Прямой код: [{converter.direct_code()}]")
        print(f"Обратный код: [{converter.reverse_code()}]")
        print(f"Дополнительный код: [{converter.additional_code()}]\n")

    @staticmethod
    def additional_code(number, bits):
        if number >= 0:
            bin_number = bin(number)[2:].zfill(bits)
        else:
            bin_number = bin((AddSub.NEGATIVE_SIGN_ADJUSTMENT << bits) + number)[AddSub.NEGATIVE_SIGN_ADJUSTMENT:]
        return bin_number[-bits:]
