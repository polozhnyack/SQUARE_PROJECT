import sqlite3

class ModuleControl:
    def __init__(self, db_name='users.db'):
        """Инициализация соединения с базой данных."""
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Создание таблицы, если она не существует."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS module_control (
                function_name TEXT PRIMARY KEY,
                is_enabled BOOLEAN NOT NULL
            )
        ''')
        self.conn.commit()

    def update_module_status(self, function_name, is_enabled):
        """Обновление состояния модуля."""
        self.cursor.execute('''
            INSERT INTO module_control (function_name, is_enabled)
            VALUES (?, ?)
            ON CONFLICT(function_name) DO UPDATE SET
                is_enabled = excluded.is_enabled
        ''', (function_name, is_enabled))
        self.conn.commit()

    def get_module_status(self, function_name):
        """Получение состояния модуля."""
        self.cursor.execute('''
            SELECT is_enabled FROM module_control
            WHERE function_name = ?
        ''', (function_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def __del__(self):
        """Закрытие соединения при удалении объекта."""
        self.conn.close()

# Пример использования класса
# if __name__ == "__main__":
#     mc = ModuleControl()

#     # Включение функции
#     mc.update_module_status('example_function', True)


