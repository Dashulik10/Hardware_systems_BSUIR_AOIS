from src.Matrix import Matrix
# Инициализируем матрицу
initial_matrix = [
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

matrix = Matrix(initial_matrix)

matrix.print_matrix()

print()
print("----------------Считываем слова по индексу: ----------------")
print()
print("Слово под индексом 0: ")
print(matrix.read_word(0, 0))
print("Слово под индексом 1: ")
print(matrix.read_word(1, 1))
print("Слово под индексом 5: ")
print(matrix.read_word(5, 5))
print("Слово под индексом 15: ")
print(matrix.read_word(15, 15))

print()
print("----------------Записываем слово по индексу 0 и 13: ----------------")
print("Слово из всех единиц.")
print()
print("Матрица после записи: ")
word = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
matrix.write_word(word, 0, 0)
matrix.write_word(word, 13, 13)
matrix.print_matrix()


print()
print("----------------Считывание разрядного столбца: ----------------")
matrix.print_matrix()
column_result = matrix.read_diagonal_column(3)
print("Столбец номер 3: ")
print(column_result)

print()
print("----------------Запись разрядного столбца на позицию 5: ----------------")
print("Столбец из всех единиц.")
print("Начальная: ")
matrix.print_matrix()
matrix.write_diagonal_column(5, word)
print("Обновленная матрица: ")
matrix.print_matrix()


print()
print("---------------- Логические Операции ----------------")
print("Например, логическая операция | Отрицание второго слова |")
print("Выполним логическую операцию над словом 7 и 8, запишем результат на место 10")
print("Начальная: ")
matrix.print_matrix()
matrix.logical_operation("not", 7, 8, 10) # not repeat const_0 const_1
print("Обновленная матрица: ")
matrix.print_matrix()


print()
print("---------------- Складывание полей ----------------")
print("Например, введём поиск по 111 ")
print("Начальная: ")
matrix.print_matrix()
print("Слово под индексом 0: ")
print(matrix.read_word(0, 0))
print("Слово под индексом 13: ")
print(matrix.read_word(13, 13))
matrix.add_fields([1, 1, 1])
print("Обновленная матрица: ")
matrix.print_matrix()
print("Слово под индексом 0: ")
print(matrix.read_word(0, 0))
print("Слово под индексом 13: ")
print(matrix.read_word(13, 13))


print()
print("---------------- Поск по соответствию ----------------")
print()
print("Все слова: ")
matrix.print_words()
search_argument = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
best_matches = matrix.search_best_match(search_argument)
print(f"Поисковый аргумент: {search_argument}")
if best_matches:
    print("Самые подходящие слова:")
    for index, word in best_matches:
        print(
            f"Индекс столбца: {index}, Слово: {word}, Количество совпадений: {sum(1 for a, b in zip(search_argument, word) if a == b)}")
else:
    print("Совпадений не найдено.")



