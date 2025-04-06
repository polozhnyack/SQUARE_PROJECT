import sqlite3

class ManagerWTF:
    def __init__(self, db_name='users.db'):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS posts_WTF (
                reddit_id TEXT PRIMARY KEY,
                subreddit TEXT,
                url TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def insert_post(self, id: str,  subreddit: str, url: str) -> bool:
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        c.execute('SELECT 1 FROM posts_WTF WHERE reddit_id = ?', (id,))
        if c.fetchone():
            conn.close()
            return False

        c.execute('''
            INSERT INTO posts_WTF (reddit_id, subreddit, url)
            VALUES (?, ?, ?)
        ''', (
            id,
            subreddit,
            url
        ))

        conn.commit()
        conn.close()
        return True
