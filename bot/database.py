import os
import sqlite3
from datetime import datetime


def init_db():
    db_path = os.path.join('..', 'data', 'users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            e_mail TEXT NOT NULL,
            password TEXT NOT NULL,
            sub BOOLEAN DEFAULT 0,
            sub_end_date TEXT,
            is_available BOOLEAN DEFAULT 0,
            notifications BOOLEAN DEFAULT 0,
            button_notifications BOOLEAN DEFAULT 0,
            last_mark TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_to_db(user_id: int, username: str, email: str, password: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, username, e_mail, password)
        VALUES (?, ?, ?, ?)
    ''', (user_id, username, email, password))
    conn.commit()
    conn.close()


def toggle_availability(user_id: int) -> bool:
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT is_available FROM users WHERE user_id = ?', (user_id,))
    current_state = cursor.fetchone()[0]
    new_state = not current_state
    cursor.execute('UPDATE users SET is_available = ? WHERE user_id = ?', (new_state, user_id))
    conn.commit()
    conn.close()
    return new_state


def toggle_notifications(user_id: int) -> bool:
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT notifications FROM users WHERE user_id = ?', (user_id,))
    current_state = cursor.fetchone()[0]
    new_state = not current_state
    cursor.execute('UPDATE users SET notifications = ? WHERE user_id = ?', (new_state, user_id))
    conn.commit()
    conn.close()
    return new_state


def toggle_button_notifications(user_id: int) -> bool:
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT button_notifications FROM users WHERE user_id = ?', (user_id,))
    current_state = cursor.fetchone()[0]
    new_state = not current_state
    cursor.execute('UPDATE users SET button_notifications = ? WHERE user_id = ?', (new_state, user_id))
    conn.commit()
    conn.close()
    return new_state


def delete_account(user_id: int):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()


def is_subscription_active(user_id: int) -> bool:
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT sub, sub_end_date FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        sub, sub_end_date = user
        if sub and sub_end_date:
            end_date = datetime.strptime(sub_end_date, '%Y-%m-%d %H:%M:%S')
            return datetime.now() <= end_date
    return False
