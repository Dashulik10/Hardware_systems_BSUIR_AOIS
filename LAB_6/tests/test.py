import unittest
from io import StringIO
import sys
from src.Hash import HashTable
from src.Record_and_AVL import AVLTree, Record


class TestHashTableDisplay(unittest.TestCase):
    def setUp(self):
        self.ht = HashTable(size=10)

    def test_display_output(self):
        self.ht.insert("Сюжет", "Последовательность событий в произведении.")
        self.ht.insert("Герой", "Действующее лицо в литературном произведении.")
        self.ht.insert("Образ", "Художественное воплощение идеи через героя, вещь, природу и др.")
        self.ht.insert("Композиция", "Структура и построение произведения.")
        self.ht.insert("Жанр", "Форма произведения (роман, рассказ, драма и т.д.).")
        self.ht.insert("Стиль", "Индивидуальная манера письма автора.")
        self.ht.insert("Мотив", "Повторяющийся элемент или образ, несущий смысл.")
        self.ht.insert("Наратор", "Голос, от имени которого ведётся повествование.")
        self.ht.insert("Аллюзия", "Скрытая отсылка к известному событию, тексту, образу.")
        self.ht.insert("Метафора", "Перенос значения по сходству (скрытое сравнение).")

        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output

        self.ht.display()

        sys.stdout = old_stdout

        expected_output_part = """
Содержимое хэш-таблицы:
+----------+------------+-----------------------------------------------------------------+
|   Индекс | Хэш        | Ключ                                                            |
+==========+============+=================================================================+
|        0 | Стиль      | Индивидуальная манера письма автора.                            |
+----------+------------+-----------------------------------------------------------------+
|        0 | Аллюзия    | Скрытая отсылка к известному событию, тексту, образу.           |
"""

        captured_text = captured_output.getvalue()
        self.assertIn(expected_output_part.strip(), captured_text)

    def test_tree_to_table_output(self):
        self.ht.insert("Сюжет", "Последовательность событий в произведении.")
        self.ht.insert("Герой", "Действующее лицо в литературном произведении.")
        self.ht.insert("Композиция", "Структура и построение произведения.")

        rows = []

        for index, tree in enumerate(self.ht.table):
            if tree.root:
                self.ht._tree_to_table(tree.root, rows, index)

        self.assertIn(
            [self.ht._hash_function("Сюжет"), "Сюжет", "Последовательность событий в произведении."],
            rows,
            "Метод _tree_to_table должен корректно добавить запись 'Сюжет'.",
        )
        self.assertIn(
            [self.ht._hash_function("Герой"), "Герой", "Действующее лицо в литературном произведении."],
            rows,
            "Метод _tree_to_table должен корректно добавить запись 'Герой'.",
        )
        self.assertIn(
            [self.ht._hash_function("Композиция"), "Композиция", "Структура и построение произведения."],
            rows,
            "Метод _tree_to_table должен корректно добавить запись 'Композиция'.",
        )

        self.assertEqual(len(rows), 3, "Должно быть 3 записи в таблице после вставки.")

class TestHashTableDisplayTreesStructure(unittest.TestCase):
    def setUp(self):
        self.ht = HashTable(size=10)

    def test_display_trees_structure(self):
        self.ht.insert("Сюжет", "Последовательность событий в произведении.")
        self.ht.insert("Герой", "Действующее лицо в литературном произведении.")
        self.ht.insert("Мотив", "Повторяющийся элемент или образ, несущий смысл.")
        self.ht.insert("Задача", "Цель, которую преследует герой в произведении.")

        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output

        self.ht.display_trees_structure()

        sys.stdout = old_stdout

        captured_text = captured_output.getvalue()

        indexes = {
            "Сюжет": self.ht._hash_function("Сюжет"),
            "Герой": self.ht._hash_function("Герой"),
            "Мотив": self.ht._hash_function("Мотив"),
            "Задача": self.ht._hash_function("Задача"),
        }

        expected_snippets = [
            f"Индекс {indexes['Мотив']}:\nКорневой узел: [Мотив] -> Повторяющийся элемент или образ, несущий смысл.\n  Левое поддерево: (пусто)\n  Правое поддерево: (пусто)",
            f"Индекс {indexes['Сюжет']}:\nКорневой узел: [Сюжет] -> Последовательность событий в произведении.\n  Левое поддерево: [Задача] -> Цель, которую преследует герой в произведении.\n  Правое поддерево: (пусто)",
            f"Индекс {indexes['Герой']}:\nКорневой узел: [Герой] -> Действующее лицо в литературном произведении.\n  Левое поддерево: (пусто)\n  Правое поддерево: (пусто)",
        ]

        for snippet in expected_snippets:
            self.assertIn(snippet, captured_text, "Структура деревьев не соответствует ожиданиям.")

class TestAVLTreeDelete(unittest.TestCase):
    def setUp(self):
        self.tree = AVLTree()

        self.tree.root = self.tree.insert(self.tree.root, Record(1, "Сюжет", "Последовательность событий."))
        self.tree.root = self.tree.insert(self.tree.root, Record(2, "Герой", "Действующее лицо."))
        self.tree.root = self.tree.insert(self.tree.root, Record(3, "Мотив", "Повторяющийся элемент."))
        self.tree.root = self.tree.insert(self.tree.root, Record(4, "Задача", "Цель героя."))

    def test_delete_leaf_node(self):
        self.tree.root = self.tree.delete(self.tree.root, "Задача")
        self.assertIsNone(self.tree.search(self.tree.root, "Задача"), "Узел с ключом 'Задача' должен быть удалён.")

    def test_delete_node_with_one_child(self):
        self.tree.root = self.tree.delete(self.tree.root, "Мотив")
        self.assertIsNone(self.tree.search(self.tree.root, "Мотив"), "Узел с ключом 'Мотив' должен быть удалён.")
        self.assertIsNotNone(self.tree.search(self.tree.root, "Герой"), "Узел 'Герой' должен остаться.")

    def test_delete_node_with_two_children(self):
        self.tree.root = self.tree.delete(self.tree.root, "Сюжет")
        self.assertIsNone(self.tree.search(self.tree.root, "Сюжет"), "Узел с ключом 'Сюжет' должен быть удалён.")

        new_root = self.tree.root
        self.assertIsNotNone(new_root, "После удаления новый корень должен быть установлен.")

        expected_key = "Задача"
        self.assertEqual(new_root.record.key, expected_key, f"Корень должен быть заменён на '{expected_key}'.")

    def test_delete_from_empty_tree(self):
        empty_tree = AVLTree()
        empty_tree.root = empty_tree.delete(empty_tree.root, "Несуществующий ключ")
        self.assertIsNone(empty_tree.root, "Пустое дерево должно оставаться пустым.")


class TestAVLTreeGetMinValueNode(unittest.TestCase):
    def setUp(self):
        self.tree = AVLTree()

        self.tree.root = self.tree.insert(self.tree.root, Record(1, "Сюжет", "Последовательность событий."))
        self.tree.root = self.tree.insert(self.tree.root, Record(2, "Герой", "Действующее лицо."))
        self.tree.root = self.tree.insert(self.tree.root, Record(3, "Мотив", "Повторяющийся элемент."))
        self.tree.root = self.tree.insert(self.tree.root, Record(4, "Задача", "Цель героя."))

    def test_get_min_value_node(self):
        min_node = self.tree.get_min_value_node(self.tree.root)
        self.assertIsNotNone(min_node, "Минимальный узел должен быть найден.")
        self.assertEqual(min_node.record.key, "Герой", "Минимальный узел должен быть узлом с ключом 'Герой'.")






if __name__ == "__main__":
    unittest.main()
