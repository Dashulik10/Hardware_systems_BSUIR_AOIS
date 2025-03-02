from logical_processing.normal_forms import NormalForms
from logical_processing.table import TruthTable


def main():
    expression = input("Введите логическое выражение: ")
    try:
        truth_table = TruthTable(expression)
        table = truth_table.generate()
        print("\nТаблица истинности:")
        for values, result in table:
            print(" | ".join([f"{int(values[var])}" for var in truth_table.variables]) + f" | {int(result)}")

        index_form = truth_table.to_index_form()
        print("\nИндексная форма:")
        print("Бинарная:", index_form["binary"])
        print("Десятичная:", index_form["decimal"])

        normal_forms = NormalForms(table, truth_table.variables)
        forms = normal_forms.compute()
        print("\nСКНФ:", forms["СКНФ"])
        print("СКНФ Индексы:", forms["СКНФ Индексы"])
        print("СДНФ:", forms["СДНФ"])
        print("СДНФ Индексы:", forms["СДНФ Индексы"])

    except ValueError as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()
