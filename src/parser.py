import requests
from bs4 import BeautifulSoup
from src.database import DatabaseRepository


class HabrParser:
    def __init__(self):
        # Заголовки для имитации браузера
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def parse_page(self, url: str = "https://habr.com/ru/feed/", max_articles: int = 10):
        """Скачивает страницу и возвращает список статей."""
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return self._parse_html(response.text, max_articles)

    def _parse_html(self, html_content: str, max_articles: int = 10):
        """Парсит HTML и извлекает только заголовок и автора."""
        soup = BeautifulSoup(html_content, 'lxml')
        parsed_data = []

        # Находим все блоки статей
        article_divs = soup.find_all('div', class_='article-snippet')

        for article_div in article_divs[:max_articles]:
            # Ищем заголовок
            title_tag = article_div.find('a', class_='tm-title__link')
            title = title_tag.get_text(strip=True)

            # Ищем автора
            author_tag = article_div.find('a', class_='tm-user-info__username')
            author = author_tag.get_text(strip=True) if author_tag else "Unknown"

            parsed_data.append({
                'title': title,
                'author': author
            })

        return parsed_data

    def save_to_db(self, parsed_data, repository: DatabaseRepository):
        """Сохраняет данные в БД. ID генерируется автоматически по порядку."""
        for index, item in enumerate(parsed_data, start=1):
            repository.add(index, item['author'], item['title'])