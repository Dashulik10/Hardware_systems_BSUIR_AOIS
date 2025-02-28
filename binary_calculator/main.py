from binary_calculator.converter import *
from binary_calculator.add_sub import *
from operations import Operations
from standart_ieee754 import StandartIEEE754


class Main:
    def menu(self):
        print("Выберите операцию: ")
        print("1. Перевести число в двоичную систему счисления.")
        print("2. Перевести число в двоичную систему в прямом коде.")
        print("3. Перевести число в двоичную систему в обратном коде.")
        print("4. Перевести число в двоичную систему в дополнительносм коде.")
        print(" ")
        print("5. Найти сумму двух чисел в дополнительном коде.")
        print("6. Найти разность двух чисел в дополнительном коде.")
        print(" ")
        print("7. Умножить два числа в прямом коде.")
        print(" ")
        print("8. Разделить с точностью до 5 знаков.")
        print("9. Найти сумму 2 положительных чисел с плавающей точкой по IEEE-754-2008")
        print("10. Выйти.")

    def run(self):
        try:
            while True:
                self.menu()
                choice = int(input("Выберите операцию: "))

                if choice in [1, 2, 3, 4]:
                    number = int(input("Введите число: "))
                    bits = int(input("Введите разрядность: "))

                    converter = Converter(number, bits)

                    if choice == 1:
                        converter.display_number_binary()
                    elif choice == 2:
                        converter.display_number_direct()
                    elif choice == 3:
                        converter.display_number_reverse()
                    elif choice == 4:
                        converter.display_number_additional()

                elif choice == 5:
                    print("Сложение:")
                    number_1 = int(input("Ввод числа №1\n"))
                    number_2 = int(input("Ввод числа №2\n"))
                    bits = int(input("Введите разрядность (по умолчанию 8): ") or 8)

                    add_sub = AddSub(number_1, number_2, bits)

                    print("Число 1:")
                    add_sub.display_number_info(number_1)
                    print("Число 2:")
                    add_sub.display_number_info(number_2)

                    result_decimal, result_additional = add_sub.add_additional()

                    add_sub.display_add_additional(result_decimal, result_additional)

                elif choice == 6:
                    print("Вычитание в дополнительном коде:")
                    number_1 = int(input("Ввод числа №1\n"))
                    number_2 = int(input("Ввод числа №2\n"))
                    bits = int(input("Введите разрядность (по умолчанию 8): ") or 8)

                    add_sub = AddSub(number_1, number_2, bits)

                    print("Число 1:")
                    add_sub.display_number_info(number_1)
                    print("Число 2:")
                    add_sub.display_number_info(number_2)

                    result_decimal, result_additional = add_sub.subtract_additional()

                    add_sub.display_add_additional(result_decimal, result_additional)

                elif choice == 7:
                    print("Умножение в прямом коде:")
                    number_1 = int(input("Ввод числа №1\n"))
                    number_2 = int(input("Ввод числа №2\n"))
                    bits = int(input("Введите разрядность (по умолчанию 8): ") or 8)

                    operstions = Operations(number_1, number_2, bits)

                    print("Число 1:")
                    operstions.display_number_info(number_1)
                    print("Число 2:")
                    operstions.display_number_info(number_2)

                    result_decimal, result_additional = operstions.multiply_direct()

                    operstions.display_mult_direct(result_decimal, result_additional)

                elif choice == 8:
                    print("Деление в прямом коде (с точностью до 5 знаков):")
                    number_1 = int(input("Ввод числа №1\n"))
                    number_2 = int(input("Ввод числа №2\n"))
                    bits = int(input("Введите разрядность (по умолчанию 8): ") or 8)

                    operstions = Operations(number_1, number_2, bits)

                    print("Число 1:")
                    operstions.display_number_info(number_1)
                    print("Число 2:")
                    operstions.display_number_info(number_2)

                    result_decimal, result_additional = operstions.binary_divide()

                    print(f"Результат деления в десятичном виде: {result_decimal}")
                    print(f"Результат деления в прямом коде: {result_additional}")

                elif choice == 9:
                    print("Сложение чисел с плавающей точкой StandartIEEE754:")
                    number_1 = float(input("Ввод числа №1\n"))
                    number_2 = float(input("Ввод числа №2\n"))

                    standart = StandartIEEE754(number_1, number_2)

                    ieee_number_1 = standart.float_to_ieee754(number_1)
                    ieee_number_2 = standart.float_to_ieee754(number_2)

                    ieee_result = standart.ieee754_addition()
                    result_float = standart.ieee754_to_float(ieee_result)

                    print(f"Число A ({number_1}) -> IEEE-754: {ieee_number_1}")
                    print(f"Число B ({number_2}) -> IEEE-754: {ieee_number_2}")
                    print(f"Сумма в IEEE-754 формате: {ieee_result}")
                    print(f"Сумма в десятичном формате: {result_float}")


                elif choice == 10:
                    print("Выход из программы.")
                    break
                else:
                    print("Неверный ввод. Попробуйте снова.")

        except ValueError:
            print("Ошибка: некорректный ввод числа.")
        except KeyboardInterrupt:
            print("\nВыход пользователем.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            print("Завершение программы.")

if __name__ == '__main__':
    program = Main()
    program.run()