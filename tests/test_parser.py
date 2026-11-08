import unittest
import os
from src.parser import HabrParser
from src.database import DatabaseRepository


class TestHabrParser(unittest.TestCase):

    def setUp(self):
        self.parser = HabrParser()
        self.db = DatabaseRepository(':memory:')

        fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'habr_page.html')
        with open(fixture_path, 'r', encoding='utf-8') as f:
            self.mock_html = f.read()

    @classmethod
    def setUpClass(cls):
        print("\n" + "=" * 60)
        print("АВТОТЕСТИРОВАНИЕ ПАРСЕРА")
        print("=" * 60)

    @classmethod
    def tearDownClass(cls):
        print("=" * 60)
        print("ЗАВЕРШЕНИЕ АВТОТЕСТИРОВАНИЯ")
        print("=" * 60 + "\n")

    def test_parse_habr_titles(self):
        print("\n[ТЕСТ 1] Извлечение заголовков и авторов из HTML-фикстуры")

        result = self.parser._parse_html(self.mock_html, max_articles=10)

        print(f"  Найдено статей: {len(result)}")
        for i, article in enumerate(result, 1):
            print(f"  [{i}] Автор: {article['author']} | Заголовок: {article['title']}")

        self.assertEqual(len(result), 4, "Ожидалось 4 статьи")

        self.assertEqual(result[0]['title'], "Первая тестовая статья про Python")
        self.assertEqual(result[0]['author'], "python_developer")

        self.assertEqual(result[1]['title'], "Вторая статья про машинное обучение")
        self.assertEqual(result[1]['author'], "ml_expert")

    def test_max_articles_limit(self):
        print("\n[ТЕСТ 2] Ограничение max_articles=2")

        result = self.parser._parse_html(self.mock_html, max_articles=2)

        print(f"  Запрошено статей: 2 | Получено: {len(result)}")
        for i, article in enumerate(result, 1):
            print(f"  [{i}] {article['title']}")

        self.assertEqual(len(result), 2, "Должно быть ровно 2 статьи")
        self.assertEqual(result[0]['title'], "Первая тестовая статья про Python")

    def test_save_to_db(self):
        print("\n[ТЕСТ 3] Сохранение распарсенных данных в БД")

        parsed_data = self.parser._parse_html(self.mock_html, max_articles=3)

        print(f"  Распарсено статей: {len(parsed_data)}")
        for article in parsed_data:
            print(f"    - {article['author']}: {article['title']}")

        self.parser.save_to_db(parsed_data, self.db)
        print("  Данные сохранены в БД")

        author_records = self.db.get_by_name("python_developer")
        print(f"  Найдено записей автора 'python_developer': {len(author_records)}")

        self.assertEqual(len(author_records), 1, "Должна быть 1 запись")
        self.assertEqual(
            author_records[0]['message'],
            "Первая тестовая статья про Python",
            "Текст сообщения должен совпадать с заголовком"
        )

if __name__ == "__main__":
    unittest.main(verbosity=2)