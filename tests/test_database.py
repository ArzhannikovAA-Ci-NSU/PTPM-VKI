import unittest
from src.database import DatabaseRepository


class TestDatabaseRepository(unittest.TestCase):

    def setUp(self):
        """Инициализация БД в оперативной памяти перед каждым тестом"""
        self.db = DatabaseRepository(':memory:')
        print(f"\n[SETUP] Создана тестовая БД в памяти.")

    def tearDown(self):
        """Очистка после теста"""
        print(f"[TEARDOWN] Тестовая БД удалена.")

    # === Тесты для метода add ===

    def test_add_success(self):
        """Успешное добавление записи"""
        print("[ТЕСТ] Успешное добавление записи")
        result = self.db.add(1, "User1", "Hello")
        self.assertTrue(result)

    def test_add_duplicate_id(self):
        """Выброс исключения при дублировании ID"""
        print("[ТЕСТ] Добавление дубликата ID (ожидается ValueError)")
        self.db.add(1, "User1", "Hello")
        with self.assertRaises(ValueError):
            self.db.add(1, "User2", "World")

    # === Тесты для метода get_by_id ===

    def test_get_by_id_success(self):
        """Успешное получение записи по ID"""
        print("[ТЕСТ] Успешное получение записи по ID")
        self.db.add(1, "User1", "Hello")
        record = self.db.get_by_id(1)
        self.assertEqual(record['name'], "User1")
        self.assertEqual(record['message'], "Hello")

    def test_get_by_id_not_found(self):
        """Возврат None при отсутствии записи"""
        print("[ТЕСТ] Получение несуществующего ID (ожидается None)")
        record = self.db.get_by_id(999)
        self.assertIsNone(record)

    # === Тесты для метода get_by_name ===

    def test_get_by_name_success(self):
        """Успешное получение списка записей по имени"""
        print("[ТЕСТ] Успешное получение списка записей по имени")
        self.db.add(1, "User1", "Hello")
        self.db.add(2, "User1", "World")
        self.db.add(3, "User2", "Test")

        records = self.db.get_by_name("User1")
        self.assertEqual(len(records), 2)

    def test_get_by_name_empty(self):
        """Возврат пустого списка при отсутствии записей"""
        print("[ТЕСТ] Получение записей по несуществующему имени")
        records = self.db.get_by_name("Nobody")
        self.assertEqual(len(records), 0)

    # === Тесты для метода update ===

    def test_update_success(self):
        """Успешное обновление сообщения"""
        print("[ТЕСТ] Успешное обновление сообщения")
        self.db.add(1, "User1", "Hello")
        result = self.db.update(1, "Updated Hello")
        self.assertTrue(result)
        self.assertEqual(self.db.get_by_id(1)['message'], "Updated Hello")

    def test_update_not_found(self):
        """Выброс исключения при обновлении несуществующего ID"""
        print("[ТЕСТ] Обновление несуществующего ID (ожидается ValueError)")
        with self.assertRaises(ValueError):
            self.db.update(999, "Test")

    # === Тесты для метода delete ===

    def test_delete_success(self):
        """Успешное удаление записи"""
        print("[ТЕСТ] Успешное удаление записи")
        self.db.add(1, "User1", "Hello")
        result = self.db.delete(1)
        self.assertTrue(result)
        self.assertIsNone(self.db.get_by_id(1))

    def test_delete_not_found(self):
        """Возврат False при удалении несуществующей записи"""
        print("[ТЕСТ] Удаление несуществующей записи")
        result = self.db.delete(999)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)