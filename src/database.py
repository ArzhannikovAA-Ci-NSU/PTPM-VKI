import sqlite3


class DatabaseRepository:
    def __init__(self, db_path: str):
        """
        Инициализация репозитория.
        :param db_path: Путь к файлу БД или ':memory:' для тестов в оперативной памяти.
        """
        self.db_path = db_path
        # Создаём ОДНО соединение и храним его
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # чтобы получать словари
        self._init_db()

    def _init_db(self):
        """Создание таблицы comments, если она еще не существует."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add(self, comment_id: int, username: str, message: str) -> bool:
        """Добавление новой записи с валидацией типов и длины."""
        # Валидация типов и длины
        if not isinstance(comment_id, int):
            raise TypeError("comment_id должен быть целым числом (int)")
        if not isinstance(username, str) or len(username) > 256:
            raise ValueError("username должен быть строкой длиной до 256 символов")
        if not isinstance(message, str) or len(message) > 8096:
            raise ValueError("message должен быть строкой длиной до 8096 символов")

        try:
            self.conn.execute(
                "INSERT INTO comments (id, name, message) VALUES (?, ?, ?)",
                (comment_id, username, message)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            raise ValueError(f"Запись с ID {comment_id} уже существует")

    def get_by_id(self, comment_id: int):
        """Получение одной записи по ID. Возвращает словарь или None."""
        cursor = self.conn.execute(
            "SELECT * FROM comments WHERE id = ?", (comment_id,)
        )
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

    def get_by_name(self, username: str):
        """Получение списка всех записей конкретного пользователя."""
        cursor = self.conn.execute(
            "SELECT * FROM comments WHERE name = ?", (username,)
        )
        return [dict(row) for row in cursor.fetchall()]

    def update(self, comment_id: int, new_message: str) -> bool:
        """Обновление текста сообщения по ID."""
        if not isinstance(new_message, str) or len(new_message) > 8096:
            raise ValueError("message должен быть строкой длиной до 8096 символов")

        cursor = self.conn.execute(
            "UPDATE comments SET message = ? WHERE id = ?",
            (new_message, comment_id)
        )
        self.conn.commit()

        if cursor.rowcount == 0:
            raise ValueError(f"Запись с ID {comment_id} не найдена")
        return True

    def delete(self, comment_id: int) -> bool:
        """Удаление записи по ID. Возвращает True, если запись была удалена."""
        cursor = self.conn.execute(
            "DELETE FROM comments WHERE id = ?", (comment_id,)
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def close(self):
        """Закрытие соединения (важно для :memory: БД)."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def __del__(self):
        """Автоматическое закрытие соединения при удалении объекта."""
        self.close()