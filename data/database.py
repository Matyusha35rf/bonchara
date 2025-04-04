import os
import sqlite3
from datetime import datetime, timedelta

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.normpath(os.path.join(script_dir, '..', 'data', 'users.db'))


# подключение к базе данных
def connect():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        return conn, cursor
    except sqlite3.Error as ex:
        print(f"Ошибка подключения к базе данных: {ex}")
        return None, None


try:
    def init_db():
        conn, cursor = connect()
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
                marked BOOLEAN DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()


    def save_to_db(user_id: int, username: str, email: str, password: str):
        conn, cursor = connect()
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, username, e_mail, password)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, email, password))
        conn.commit()
        conn.close()


    def sw_av(user_id: int) -> bool:
        conn, cursor = connect()
        cursor.execute('SELECT is_available FROM users WHERE user_id = ?', (user_id,))
        current_state = cursor.fetchone()[0]
        new_state = not current_state
        cursor.execute('UPDATE users SET is_available = ? WHERE user_id = ?', (new_state, user_id))
        conn.commit()
        conn.close()
        return new_state


    def sw_notif(user_id: int) -> bool:
        conn, cursor = connect()
        cursor.execute('SELECT notifications FROM users WHERE user_id = ?', (user_id,))
        current_state = cursor.fetchone()[0]
        new_state = not current_state
        cursor.execute('UPDATE users SET notifications = ? WHERE user_id = ?', (new_state, user_id))
        conn.commit()
        conn.close()
        return new_state


    def sw_butt_notif(user_id: int) -> bool:
        conn, cursor = connect()
        cursor.execute('SELECT button_notifications FROM users WHERE user_id = ?', (user_id,))
        current_state = cursor.fetchone()[0]
        new_state = not current_state
        cursor.execute('UPDATE users SET button_notifications = ? WHERE user_id = ?', (new_state, user_id))
        conn.commit()
        conn.close()
        return new_state

    # обновление айдишников
    def reset_ids():
        conn, cursor = connect()
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


    def del_acc(user_id: int):
        conn, cursor = connect()
        cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
        reset_ids()

    # активация/продление подписки
    def sub(user_id: int, months: int) -> bool:
        conn, cursor = connect()
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
            cursor.execute('UPDATE users SET sub = ? WHERE user_id = ?', (True, user_id))

        # Добавляем количество месяцев (30 дней * months)
        new_sub_end_date = current_date + timedelta(days=30 * months)

        # Обновляем дату окончания подписки в базе данных
        cursor.execute('''
            UPDATE users
            SET sub_end_date = ?
            WHERE user_id = ?
        ''', (new_sub_end_date.strftime('%Y-%m-%d'), user_id))

        conn.commit()
        conn.close()
        return True


    def is_sub_activ(user_id: int) -> bool:
        conn, cursor = connect()
        cursor.execute('SELECT sub FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user[0]

    # деактивация подписки
    def sub_deactiv(user_id: int) -> bool:
        conn, cursor = connect()
        cursor.execute('UPDATE users SET sub = ? WHERE user_id = ?', (False, user_id))
        conn.commit()
        conn.close()
        return True


    def read_db(filename):
        '''
        Чтение бд
        :param filename:
        :return: conn, cursor
        '''
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        return conn, cursor


    def get_users(cursor):
        '''
        Получение списка пользователей из бд
        :param cursor:
        :return: users
        '''
        src = cursor.execute("SELECT * FROM users").fetchall()
        headers = [i[1] for i in cursor.execute("PRAGMA table_info(users)").fetchall()]
        users = [dict(zip(headers, row)) for row in src]
        return users


    def marked_off(con, cur, now):
        '''
        Перевод информации об отметке в False
        :param con:
        :param cur:
        :param now:
        :return:
        '''
        print(f"Отметки сброшены в {now}")
        cur.execute(
            f'''UPDATE users
                SET marked = 0''')
        con.commit()


    def marked_on(con, cur, user_id):
        '''
        Перевод информации об отметке определенного пользователя в True
        :param con:
        :param cur:
        :param user_id:
        :return:
        '''
        cur.execute(
            f'''UPDATE users
             SET marked = 1
             WHERE user_id = {user_id}''')
        con.commit()


except sqlite3.Error as e:
    print(f"Ошибка при выполнении запроса в бд: {e}")
except Exception as e:
    print(f"Ошибка: {e}")
