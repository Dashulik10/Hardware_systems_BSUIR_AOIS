class Converter:
    def __init__(self, number, bits=8):
        self.number = number
        self.bits = bits

    def make_it_binary(self):
        if self.number >= 0:
            binary = ""
            for i in range(self.bits - 1, -1, -1):
                binary += "1" if (self.number & (1 << i)) else "0"
            return binary
        else:
            raise ValueError("Number must be positive")

    def display_number_binary(self):
        binary_number = self.make_it_binary()
        print(f"Десятичное: {self.number}")
        print(f"Двоичное: {binary_number}")
        print(" ")

    def direct_code(self):
        sign = "0" if self.number >= 0 else "1"
        abs_value = abs(self.number)
        direct = Converter(abs_value, self.bits - 1).make_it_binary()
        return f"{sign} {direct}"

    def display_number_direct(self):
        print(f"Десятичное: {self.number}")
        print(f"Прямой код: {self.direct_code()}")

    def reverse_code(self):
        if self.number >= 0:
            return self.direct_code()
        abs_value = abs(self.number)
        direct = Converter(abs_value, self.bits - 1).make_it_binary()
        reverse = ''.join('1' if bit == '0' else '0' for bit in direct)
        return f"1 {reverse}"

    def display_number_reverse(self):
        print(f"Десятичное: {self.number}")
        print(f"Обратный код: {self.reverse_code()}")

    def additional_code(self):
        if self.number >= 0:
            direct = self.direct_code().split(" ")[1]
            return f"0 {direct.zfill(self.bits - 1)}"

        reverse = self.reverse_code().split(" ")[1]
        initial_carry = 1
        additional = ""
        for bit in reversed(reverse):
            if bit == "1" and initial_carry == 1:
                additional = "0" + additional
            elif bit == "0" and initial_carry == 1:
                additional = "1" + additional
                initial_carry = 0
            else:
                additional = bit + additional
        return f"1 {additional.zfill(self.bits - 1)}"

    def display_number_additional(self):
        print(f"Десятичное: {self.number}")
        print(f"Дополнительный код: {self.additional_code()}")




    def display_number_info(self):
        print(f"Число введено: {self.number}")
        print(f"Прямой код: [{self.direct_code()}]")
        print(f"Обратный код: [{self.reverse_code()}]")
        print(f"Дополнительный код: [{self.additional_code()}]\n")

    def display_add_additional(self, result_decimal, result_additional, bits=8):
        converter = Converter(result_decimal, bits)
        print(f"Результат: {result_decimal}")
        print(f"Прямой код: [{converter.direct_code()}]")
        print(f"Обратный код: [{converter.reverse_code()}]")
        print(f"Дополнительный код: {result_additional}\n")

    def display_mult_direct(self, result_decimal, result_direct, bits=8):
        converter = Converter(result_decimal, bits)
        print(f"Результат: {result_decimal}")
        print(f"Прямой код: {result_direct}")
        print(f"Обратный код: [{converter.reverse_code()}]")
        print(f"Дополнительный код: [{converter.additional_code()}]")



