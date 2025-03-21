from logical_processing.min import Minimizing
from logical_processing.normal_forms import NormalForms
from logical_processing.table import TruthTableWithSubexpressions

def main():
    expression = input("Введите логическое выражение: ")
    try:
        # Шаг 1: Генерация таблицы истинности
        tt = TruthTableWithSubexpressions(expression)
        tt.display_table()

        # Шаг 2: Вывод индексной формы
        index_form = tt.to_index_form()
        print("\nИндексная форма:")
        print("Бинарная:", index_form["binary"])
        print("Десятичная:", index_form["decimal"])

        # Шаг 3: Вычисление СКНФ и СДНФ
        truth_table = tt.generate_table()  # Генерируем таблицу
        normal_forms = NormalForms(truth_table, tt.variables)
        forms = normal_forms.compute()
        print("\nСКНФ:", forms["СКНФ"])
        print("СКНФ Индексы:", forms["СКНФ Индексы"])
        print("СДНФ:", forms["СДНФ"])
        print("СДНФ Индексы:", forms["СДНФ Индексы"])

    except ValueError as e:
        print("Ошибка:", e)

if __name__ == "__main__":
    main()
