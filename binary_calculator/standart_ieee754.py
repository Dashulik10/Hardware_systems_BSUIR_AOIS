class StandartIEEE754:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def float_to_ieee754(self, num):
        sign = '1' if num < 0 else '0'
        if num == 0:
            return '0' * 32

        num = abs(num)
        int_part = int(num)
        frac_part = num - int_part
        int_bin = bin(int_part)[2:] if int_part > 0 else ''
        frac_bin = ''

        while frac_part and len(frac_bin) < 23:
            frac_part *= 2
            bit = int(frac_part)
            frac_bin += str(bit)
            frac_part -= bit

        # Определяем экспоненту
        if int_bin:
            exp = len(int_bin) - 1
        elif '1' in frac_bin:
            exp = -frac_bin.index('1') - 1
        else:
            return '0' * 32  # Ноль

        exp_bits = bin(exp + 127)[2:].zfill(8)
        mantissa_bits = (int_bin[1:] + frac_bin).ljust(23, '0')[:23]

        return f'{sign}{exp_bits}{mantissa_bits}'

    def ieee754_to_float(self, ieee_bin):
        sign = int(ieee_bin[0])
        exp = int(ieee_bin[1:9], 2) - 127
        mantissa = ieee_bin[9:]

        if exp == -127:
            mantissa_value = 0.0
            for i, bit in enumerate(mantissa):
                if bit == '1':
                    mantissa_value += 2 ** -(i + 1)
            result = mantissa_value * (2 ** -126)
        else:
            mantissa_value = 1.0
            for i, bit in enumerate(mantissa):
                if bit == '1':
                    mantissa_value += 2 ** -(i + 1)
            result = mantissa_value * (2 ** exp)

        return -result if sign else result

    def ieee754_addition(self):
        a_ieee = self.float_to_ieee754(self.num1)
        b_ieee = self.float_to_ieee754(self.num2)

        # Разбираем
        sign_a, exp_a, mant_a = int(a_ieee[0]), int(a_ieee[1:9], 2), int('1' + a_ieee[9:], 2)
        sign_b, exp_b, mant_b = int(b_ieee[0]), int(b_ieee[1:9], 2), int('1' + b_ieee[9:], 2)

        # Выравниваем
        if exp_a > exp_b:
            shift = exp_a - exp_b
            mant_b >>= shift
            exp_b = exp_a
        elif exp_b > exp_a:
            shift = exp_b - exp_a
            mant_a >>= shift
            exp_a = exp_b

        if sign_a:
            mant_a = -mant_a
        if sign_b:
            mant_b = -mant_b

        # Складываем мантиссы
        mant_sum = mant_a + mant_b
        sign_res = 0 if mant_sum >= 0 else 1
        mant_sum = abs(mant_sum)
        exp_res = exp_a


        if mant_sum == 0:
            return '0' * 32

        while mant_sum and not (mant_sum & (1 << 23)):
            mant_sum <<= 1
            exp_res -= 1

        if mant_sum & (1 << 24):
            mant_sum >>= 1
            exp_res += 1

        if exp_res <= 0:
            exp_res = 0
            mant_sum = 0
        elif exp_res >= 255:
            exp_res = 255
            mant_sum = 0

        mantissa_bits = bin(mant_sum)[3:26].ljust(23, '0')
        exp_bits = bin(exp_res)[2:].zfill(8)

        return f'{sign_res}{exp_bits}{mantissa_bits}'

    def sum_of_binary_ieee754(self):
        num1 = self.float_to_ieee754(self.num1)
        num2 = self.float_to_ieee754(self.num2)
        return self.ieee754_addition()
