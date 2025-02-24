import sqlite3
import os
from datetime import datetime, timedelta


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
            marked TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_to_db(user_id: int, username: str, email: str, password: str):
    db_path = os.path.join('..', 'data', 'users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, username, e_mail, password)
        VALUES (?, ?, ?, ?)
    ''', (user_id, username, email, password))
    conn.commit()
    conn.close()


def toggle_availability(user_id: int) -> bool:
    db_path = os.path.join('..', 'data', 'users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT is_available FROM users WHERE user_id = ?', (user_id,))
    current_state = cursor.fetchone()[0]
    new_state = not current_state
    cursor.execute('UPDATE users SET is_available = ? WHERE user_id = ?', (new_state, user_id))
    conn.commit()
    conn.close()
    return new_state


def toggle_notifications(user_id: int) -> bool:
    db_path = os.path.join('..', 'data', 'users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT notifications FROM users WHERE user_id = ?', (user_id,))
    current_state = cursor.fetchone()[0]
    new_state = not current_state
    cursor.execute('UPDATE users SET notifications = ? WHERE user_id = ?', (new_state, user_id))
    conn.commit()
    conn.close()
    return new_state


def toggle_button_notifications(user_id: int) -> bool:
    db_path = os.path.join('..', 'data', 'users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT button_notifications FROM users WHERE user_id = ?', (user_id,))
    current_state = cursor.fetchone()[0]
    new_state = not current_state
    cursor.execute('UPDATE users SET button_notifications = ? WHERE user_id = ?', (new_state, user_id))
    conn.commit()
    conn.close()
    return new_state


# обновление айдишников
def reset_ids():
    db_path = os.path.join('..', 'data', 'users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Получаем все записи, отсортированные по id
    cursor.execute('SELECT * FROM users ORDER BY id')
    users = cursor.fetchall()
    # Обновляем id, начиная с 1
    for new_id, user in enumerate(users, start=1):
        old_id = user[0]  # id находится на индексе 0 (первый столбец)
        cursor.execute('UPDATE users SET id = ? WHERE id = ?', (new_id, old_id))

    # Сбрасываем значение автоинкремента
    cursor.execute('DELETE FROM sqlite_sequence WHERE name = "users"')
    cursor.execute('INSERT INTO sqlite_sequence (name, seq) VALUES ("users", ?)', (len(users),))
    conn.commit()
    conn.close()

print(reset_ids())

def del_acc(user_id: int):
    print(0)
    db_path = os.path.join('..', 'data', 'users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    reset_ids()


# активация/продление подписки
def sub(user_id: int, months: int) -> bool:
    db_path = os.path.join('..', 'data', 'users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Получаем текущую дату окончания подписки
        cursor.execute('SELECT sub_end_date FROM users WHERE user_id = ?', (user_id,))

        result = cursor.fetchone()
        if result is None:
            # Если пользователь не найден, возвращаем False
            return False

        current_sub_end_date = result[0]  # Текущая дата окончания подписки

        # Вычисляем новую дату окончания подписки
        if current_sub_end_date:
            current_date = datetime.strptime(current_sub_end_date, '%Y-%m-%d')
        else:
            current_date = datetime.now()
            sub_activ(user_id)

        # Добавляем количество месяцев (30 дней * months)
        new_sub_end_date = current_date + timedelta(days=30 * months)

        # Обновляем дату окончания подписки в базе данных
        cursor.execute('''
            UPDATE users
            SET sub_end_date = ?
            WHERE user_id = ?
        ''', (new_sub_end_date.strftime('%Y-%m-%d'), user_id))

        conn.commit()
        return True

    except Exception as e:
        print(f"Ошибка при обновлении подписки: {e}")
        return False

    finally:
        conn.close()


def is_sub_activ(user_id: int) -> bool:
    db_path = os.path.join('..', 'data', 'users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT sub FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user[0]


# активация подписки
def sub_activ(user_id: int) -> bool:
    db_path = os.path.join('..', 'data', 'users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET sub = ? WHERE user_id = ?', (True, user_id))
    conn.commit()
    conn.close()
    return True


# деактивация подписки
def sub_deactiv(user_id: int) -> bool:
    db_path = os.path.join('..', 'data', 'users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET sub = ? WHERE user_id = ?', (False, user_id))
    conn.commit()
    conn.close()
    return True
