from logical_parser import LogicParser
from table import TruthTable
from normal_forms import NormalForms

def main():
    while True:
        try:
            expression = input("Введите логическую функцию: ")
            parser = LogicParser(expression)
            parsed_expr = parser.parse()
            variables = parser.variables
            break
        except ValueError as e:
            print(e)
            print("Попробуйте снова.")

    truth_table = TruthTable(parsed_expr, variables)
    table = truth_table.generate()
    truth_table.display()

    normal_forms = NormalForms(table, variables)

    print_result("СДНФ", normal_forms.get_sdnf())
    print_result("СКНФ", normal_forms.get_sknf())
    print_result("Числовая форма СДНФ", normal_forms.get_numeric_sdnf())
    print_result("Числовая форма СКНФ", normal_forms.get_numeric_sknf())


def print_result(title, result):
    print(f"{title}: {result}\n")

if __name__ == "__main__":
    main()