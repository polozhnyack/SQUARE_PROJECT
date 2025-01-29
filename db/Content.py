import sqlite3

class VideoDatabase:
    def __init__(self, db_name='users.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Создает таблицу для хранения видео."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            video_id TEXT NOT NULL,
            site TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            tags TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.conn.commit()

    def insert_video(self, url, video_id, site, title, description, tags):
        """Вставка нового видео в базу данных."""
        self.cursor.execute("""
        INSERT INTO videos (url, video_id, site, title, description, tags)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (url, video_id, site, title, description, tags))
        self.conn.commit()

    def get_video_by_url(self, url):
        """Получение видео по URL."""
        self.cursor.execute("SELECT * FROM videos WHERE url=?", (url,))
        return self.cursor.fetchone()

    def get_all_videos(self):
        """Получение всех видео из базы."""
        self.cursor.execute("SELECT * FROM videos")
        return self.cursor.fetchall()

    def update_video(self, url, title=None, description=None, tags=None):
        """Обновление информации о видео."""
        if title:
            self.cursor.execute("UPDATE videos SET title=? WHERE url=?", (title, url))
        if description:
            self.cursor.execute("UPDATE videos SET description=? WHERE url=?", (description, url))
        if tags:
            self.cursor.execute("UPDATE videos SET tags=? WHERE url=?", (tags, url))
        self.conn.commit()

    def close(self):
        """Закрытие соединения с базой данных."""
        self.conn.close()

