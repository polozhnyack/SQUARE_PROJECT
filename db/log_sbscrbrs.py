import sqlite3

def log_subscriber(user_id, username, full_name, first_name, last_name, is_bot, phone_number, bio, chat_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR IGNORE INTO channel_join_requests 
        (user_id, username, full_name, first_name, last_name, is_bot, phone_number, bio, chat_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, username, full_name, first_name, last_name, is_bot, phone_number, bio, chat_id))
    
    conn.commit()
    conn.close()

