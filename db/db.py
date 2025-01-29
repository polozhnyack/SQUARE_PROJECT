import sqlite3

class Database:
    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE,
                    first_name TEXT,
                    last_name TEXT
                )
            """)

    def add_user(self, user_id, first_name, last_name):
        try:
            with self.conn:
                self.conn.execute("INSERT OR IGNORE INTO users (user_id, first_name, last_name) VALUES (?, ?, ?)",
                                  (user_id, first_name, last_name))
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении пользователя: {e}")

    def remove_user(self, user_id):
        try:
            with self.conn:
                self.conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        except sqlite3.Error as e:
            print(f"Ошибка при удалении пользователя: {e}")

    def get_user(self, user_id):
        try:
            with self.conn:
                return self.conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
        except sqlite3.Error as e:
            print(f"Ошибка при получении пользователя: {e}")
            return None

    def get_all_users(self):
        try:
            with self.conn:
                return self.conn.execute("SELECT * FROM users").fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка при получении всех пользователей: {e}")
            return []

    def close(self):
        if self.conn:
            self.conn.close()
