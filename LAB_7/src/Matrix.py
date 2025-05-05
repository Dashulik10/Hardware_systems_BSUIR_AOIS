class Matrix:
    def __init__(self, initial_matrix):
        self.rows = len(initial_matrix)
        self.cols = len(initial_matrix[0])
        self.matrix = initial_matrix


    def print_matrix(self):
        print("\nМатрица:")
        for row in self.matrix:
            print(row)

    def read_word(self, start_row, start_col):
        word = []
        for i in range(self.rows):
            row = (start_row + i) % self.rows
            word.append(self.matrix[row][start_col])
        return word

    def write_word(self, word, start_row, start_col):
        if len(word) != self.rows:
            raise ValueError("Слово должно быть длиной, равной числу строк.")

        for i in range(len(word)):
            row = (start_row + i) % self.rows
            self.matrix[row][start_col] = word[i]

    def print_words(self):
        print("\nВсе слова (по столбцам):")
        for col in range(self.cols):
            start_row = col
            word = self.read_word(start_row, col)
            print(f"S_{col} (startRow={start_row}): {word}")

    def read_diagonal_column(self, start_index):
        result = []
        row, col = start_index, 0

        for _ in range(self.rows):
            result.append(str(self.matrix[row][col]))
            row = (row + 1) % self.rows
            col = (col + 1) % self.cols

        return ''.join(result)

    def write_diagonal_column(self, start_index, new_column):
        if len(new_column) != self.rows:
            raise ValueError("Длина нового столбца должна быть равна числу строк в матрице.")

        row, col = start_index, 0

        for i in range(len(new_column)):
            self.matrix[row][col] = int(new_column[i])
            row = (row + 1) % self.rows
            col = (col + 1) % self.cols


    def logical_operation(self, operation, word_1_col, word_2_col, result_col):
        word_1 = self.read_word(0, word_1_col)
        word_2 = self.read_word(0, word_2_col)

        result_word = []

        for bit_1, bit_2 in zip(word_1, word_2):
            if operation == "repeat":
                result_bit = bit_2
            elif operation == "not":
                result_bit = 1 - bit_2
            elif operation == "const_0":
                result_bit = 0
            elif operation == "const_1":
                result_bit = 1
            else:
                raise ValueError(f"Операция {operation} не поддерживается.")
            result_word.append(result_bit)

        self.write_word(result_word, 0, result_col)


    def add_binary_numbers(self, a, b):
        carry = 0
        max_len = max(len(a), len(b))
        result = [0] * (max_len + 1)

        for i in range(max_len):
            bit_a = a[-1 - i] if i < len(a) else 0
            bit_b = b[-1 - i] if i < len(b) else 0
            total = bit_a + bit_b + carry
            result[-1 - i] = total % 2
            carry = total // 2

        if carry:
            result[0] = 1

        if result[0] == 0:
            result = result[1:]
        return result

    def add_fields(self, v_filter):
        if len(v_filter) != 3 or any(bit not in [0, 1] for bit in v_filter):
            raise ValueError("v_filter должен быть списком из 3 битов (состоящий из 0 и 1).")

        for col in range(self.cols):
            for row_offset in range(self.rows):
                row = (col + row_offset) % self.rows

                word = self.read_word(row, col)

                v_bits = word[:3]
                if v_bits != v_filter:
                    continue

                a_bits = word[3:7]
                b_bits = word[7:11]
                s_bits = word[11:]

                sum_result = self.add_binary_numbers(a_bits, b_bits)

                while len(sum_result) < 5:
                    sum_result.insert(0, 0)

                updated_word = v_bits + a_bits + b_bits + sum_result[:5]

                self.write_word(updated_word, row, col)

                break

    def search_best_match(self, search_argument):
        if len(search_argument) != 16:
            raise ValueError("Поисковый аргумент должен состоять из 16 битов.")

        max_matches = -1
        best_matches = []

        print("\nВсе слова (по столбцам):")
        for col in range(self.cols):
            word = self.read_word(0, col)

            matches = sum(1 for arg_bit, word_bit in zip(search_argument, word) if arg_bit == word_bit)

            if matches > max_matches:
                max_matches = matches
                best_matches = [(col, word)]
            elif matches == max_matches:
                best_matches.append((col, word))

        return best_matches










