from logical_processing.KarnaughMinimizer import KarnaughMinimizer
from logical_processing.min import Minimizing
from logical_processing.normal_forms import NormalForms
from logical_processing.table import TruthTableWithSubexpressions

def main():
    expression = input("Введите логическое выражение: ")
    try:
        # 2 ЛАБА
        tt = TruthTableWithSubexpressions(expression)
        tt.display_table()

        #index_form = tt.to_index_form()
        #print("\nИндексная форма:")
        #print("Бинарная:", index_form["binary"])
        #print("Десятичная:", index_form["decimal"])

        truth_table = tt.generate_table()
        normal_forms = NormalForms(truth_table, tt.variables)
        forms = normal_forms.compute()
        print("\nСДНФ:", forms["СДНФ"])
        #print("СДНФ Индексы:", forms["СДНФ Индексы"])
        print("СКНФ:", forms["СКНФ"])
        #print("СКНФ Индексы:", forms["СКНФ Индексы"])

        # ПЕРВЫЙ МЕТОД - РАСЧЁТНЫЙ
        print("\n============================================ МЕТОД 1 ============================================")

        variables = tt.variables

        expression_d = forms["СДНФ"]
        result_d = Minimizing.terms_sdnf(expression_d)
        print("\nСДНФ ТЕРМЫ: ", result_d)
        min_d = Minimizing.minimize_sdnf(result_d, variables)

        # Шаг 5:
        expression_k = forms["СКНФ"]
        result_k = Minimizing.terms_sknf(expression_k)
        print("\nСКНФ ТЕРМЫ: ", result_k)
        min_k = Minimizing.minimize_sknf(result_k, variables)







        # ВТОРОЙ МЕТОД - РАСЧЁТНО-ТАБЛИЧНЫЙ
        print("\n============================================ МЕТОД 2 ============================================")
        min_d2 = Minimizing.minimize_sdnf_second(result_d, variables)
        print("\n====================== ТАБЛИЦА ======================")
        Minimizing.build_sdnf_table(result_d, min_d2)

        min_k2 = Minimizing.minimize_sknf_second(result_k, variables)
        print("\n====================== ТАБЛИЦА ======================")
        Minimizing.build_sknf_table(result_k, min_k2)



        # ТРЕТИЙ МЕТОД - КАРТА КАРНО
        print("\n============================================ МЕТОД 3 ============================================")
        print("\n============================================ СДНФ ============================================")
        karnaugh_minimizer = KarnaughMinimizer(expression_d)
        karnaugh_minimizer.generate_simplified_table()
        karnaugh_minimizer.display_simplified_table()
        karnaugh_minimizer.display_karnaugh_map()
        minimized_sdnf = karnaugh_minimizer.minimize_sdnf()
        print("\nМинимизированная СДНФ:")
        print(minimized_sdnf)

        print("\n============================================ СKНФ ============================================")
        karnaugh_minimizer = KarnaughMinimizer(expression_d)
        karnaugh_minimizer.generate_simplified_table()
        karnaugh_minimizer.display_simplified_table()
        karnaugh_minimizer.display_karnaugh_map()
        minimized_sknf = karnaugh_minimizer.minimize_sknf()
        print("\nМинимизированная СКНФ:")
        print(minimized_sknf)




    except ValueError as e:
        print("Ошибка:", e)

if __name__ == "__main__":
    main()
