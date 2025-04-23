import os
import sqlite3
from datetime import datetime, timedelta

import lk.match_groups

# Определение путей к базам данных
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.normpath(os.path.join(script_dir, '..', 'data', 'users.db'))


def connect():
    """
    Устанавливает соединение с основной базой данных.

    :return: Кортеж из объекта соединения и курсора, либо (None, None) при ошибке
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        return conn, cursor
    except sqlite3.Error as ex:
        print(f"Ошибка подключения к базе данных: {ex}")
        return None, None


def init_db():
    """
    Инициализирует основную таблицу пользователей.
    Создает базу данных со всеми необходимыми таблицами, если они не существуют.
    """
    conn, cursor = connect()
    try:
        # Основная таблица
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                username TEXT,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                sub BOOLEAN DEFAULT 0,
                sub_end_date TEXT,
                av_status BOOLEAN DEFAULT 1,
                button_notifications BOOLEAN DEFAULT 1,
                marked BOOLEAN DEFAULT 0,
                user_group TEXT,
                semester INT
            )
        ''')
        # Таблица предметов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                status BOOLEAN DEFAULT 1,
                UNIQUE(subject, user_id)
            )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_name TEXT UNIQUE NOT NULL,
        group_id INTEGER NOT NULL)
        ''')
        lk.match_groups.write_db()


        cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule_today (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_name TEXT NOT NULL,
        lesson_num TEXT NOT NULL,
        lesson_title TEXT NOT NULL,
        teacher TEXT,
        auditorium TEXT,
        lesson_type TEXT
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        minutes_10 BOOLEAN DEFAULT 0,
        minutes_15 BOOLEAN DEFAULT 0,
        minutes_20 BOOLEAN DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        )''')

        # ---- Добавление триггера при котором при добавлении пользователя в users автоматически добавляется в уведомления ----
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS create_notification_after_user_insert
            AFTER INSERT ON users
            BEGIN
                INSERT INTO notifications (user_id, minutes_10, minutes_15, minutes_20)
                VALUES (NEW.user_id, 0, 0, 0);
            END;
        ''')

        conn.commit()
    finally:
        conn.close()


def add_to_db_reg(user_id: int, username: str, email: str, password: str,
                  user_group: str, semester: int):
    """Добавляет или обновляет данные пользователя при регистрации.

    :param user_id: ID пользователя в Telegram
    :param username: Имя пользователя в Telegram
    :param email: Электронная почта пользователя
    :param password: Пароль пользователя
    :param user_group: Группа пользователя
    :param semester: Номер семестра пользователя
    """
    conn, cursor = connect()
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, username, email, password, user_group, semester)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, username, email, password, user_group, semester))
        conn.commit()
    finally:
        conn.close()


def sw_av(user_id: int) -> bool:
    """Переключает статус автопосещения пользователя.

    :param user_id: ID пользователя в Telegram
    :return: Новое состояние автопосещения
    """
    conn, cursor = connect()
    try:
        cursor.execute('SELECT av_status FROM users WHERE user_id = ?', (user_id,))
        current_state = cursor.fetchone()[0]
        new_state = not current_state
        cursor.execute('UPDATE users SET av_status = ? WHERE user_id = ?', (new_state, user_id))
        conn.commit()
        return new_state
    finally:
        conn.close()


def sw_notif(user_id: int) -> bool:
    """
    Переключает статус уведомлений пользователя.

    :param user_id: ID пользователя в Telegram
    :return: Новое состояние уведомлений
    """
    conn, cursor = connect()
    try:
        cursor.execute('SELECT notifications FROM users WHERE user_id = ?', (user_id,))
        current_state = cursor.fetchone()[0]
        new_state = not current_state
        cursor.execute('UPDATE users SET notifications = ? WHERE user_id = ?', (new_state, user_id))
        conn.commit()
        return new_state
    finally:
        conn.close()


def sw_butt_notif(user_id: int) -> bool:
    """
    Переключает статус уведомлений о кнопках.

    :param user_id: ID пользователя в Telegram
    :return: Новое состояние уведомлений о кнопках
    """
    conn, cursor = connect()
    try:
        cursor.execute('SELECT button_notifications FROM users WHERE user_id = ?', (user_id,))
        current_state = cursor.fetchone()[0]
        new_state = not current_state
        cursor.execute('UPDATE users SET button_notifications = ? WHERE user_id = ?', (new_state, user_id))
        conn.commit()
        return new_state
    finally:
        conn.close()


def del_acc(user_id: int):
    """
    Удаляет аккаунт пользователя.

    :param user_id: ID пользователя в Telegram
    """
    conn, cursor = connect()
    try:
        cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        conn.commit()
    finally:
        conn.close()


def sub(user_id: int, months: int) -> bool:
    """
    Активирует или продлевает подписку пользователя.

    :param user_id: ID пользователя в Telegram
    :param months: Количество месяцев подписки
    :return: True если операция успешна, False если пользователь не найден
    """
    conn, cursor = connect()
    try:
        cursor.execute('SELECT sub_end_date FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result is None:
            return False

        current_sub_end_date = result[0]

        if current_sub_end_date:
            current_date = datetime.strptime(current_sub_end_date, '%Y-%m-%d')
        else:
            current_date = datetime.now()
            cursor.execute('UPDATE users SET sub = ? WHERE user_id = ?', (True, user_id))

        new_sub_end_date = current_date + timedelta(days=30 * months)

        cursor.execute('''
            UPDATE users SET sub_end_date = ? WHERE user_id = ?
        ''', (new_sub_end_date.strftime('%Y-%m-%d'), user_id))

        conn.commit()
        return True
    finally:
        conn.close()


def is_sub_activ(user_id: int) -> bool:
    """
    Проверяет активна ли подписка пользователя.

    :param user_id: ID пользователя в Telegram
    :return: Состояние подписки
    """
    conn, cursor = connect()
    try:
        cursor.execute('SELECT sub FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        return user[0]
    finally:
        conn.close()


def sub_deactiv(user_id: int) -> bool:
    """
    Деактивирует подписку пользователя.

    :param user_id: ID пользователя в Telegram
    :return: Всегда возвращает True
    """
    conn, cursor = connect()
    try:
        cursor.execute('''UPDATE users
                      SET sub = ?,
                      sub_end_date = ?
                      WHERE user_id = ?''', (False, '', user_id))
        conn.commit()
        return True
    finally:
        conn.close()


def get_users(cursor) -> list:
    """
    Возвращает список всех пользователей.

    :param cursor: Курсор базы данных
    :return: Список словарей с информацией о пользователях
    """
    src = cursor.execute("SELECT * FROM users").fetchall()
    headers = [i[1] for i in cursor.execute("PRAGMA table_info(users)").fetchall()]
    return [dict(zip(headers, row)) for row in src]


def get_user(user_id):
    """

    :param user_id: ID пользователя в Telegram
    :return: Словарь с данными пользователя или None, если пользователь не найден
    """
    con, cur = connect()

    # Получаем данные пользователя и информацию о столбцах за один запрос
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user_data = cur.fetchone()

    if user_data:
        # Получаем названия столбцов из cursor.description
        columns = [column[0] for column in cur.description]
        user_dict = dict(zip(columns, user_data))
        con.close()
        return user_dict

    con.close()
    return None


def marked_off(con, cur, now):
    """
    Сбрасывает все отметки пользователей.

    :param con: Соединение с БД
    :param cur: Курсор БД
    :param now: Время выполнения операции
    """
    print(f"Отметки сброшены в {now}")
    cur.execute('''UPDATE users SET marked = 0''')
    con.commit()


def marked_on(con, cur, user_id: int):
    """
    Устанавливает отметку для конкретного пользователя.

    :param con: Соединение с БД
    :param cur: Курсор БД
    :param user_id: ID пользователя в Telegram
    """
    cur.execute('''UPDATE users SET marked = 1 WHERE user_id = ?''', (user_id,))
    con.commit()


def add_to_db_subjects(user_id: int, subjects: set):
    """
    Добавляет предметы для пользователя.

    :param user_id: ID пользователя в Telegram
    :param subjects: Список предметов
    """
    conn, cur = connect()
    try:
        for subject in subjects:
            cur.execute('''
                INSERT OR REPLACE INTO subjects (subject, user_id)
                VALUES (?, ?)
            ''', (subject, user_id))
        conn.commit()
    finally:
        conn.close()


def get_subjects_status(user_id):
    """
    Возвращает словарь {subject_name: status} для пользователя

    :param user_id: ID пользователя в Telegram
    :return: словарь предметов с их статусом
    """
    con, cur = connect()
    cur.execute('''
        SELECT subject, status FROM subjects 
        WHERE user_id = ?
    ''', (user_id,))
    rows = cur.fetchall()
    con.commit()
    con.close()
    return {row[0]: bool(row[1]) for row in rows}


def del_subjects(user_id: int, subjects):
    """
    Удаляет предмет для пользователя.

    :param user_id: ID пользователя в Telegram
    :param subjects: Название предмета
    """
    conn, cur = connect()
    try:
        for subject in subjects:
            cur.execute('DELETE FROM subjects WHERE user_id = ? AND subject = ?', (user_id, subject))
        conn.commit()
    finally:
        conn.close()


def sw_subject_status(user_id: int, subject: str) -> bool:
    """
    Переключает состояние предмета (включен/выключен) для пользователя.

    :param user_id: ID пользователя в Telegram
    :param subject: Название предмета
    :return: Новое состояние предмета (True - включен, False - выключен)
    """
    conn, cursor = connect()
    try:
        cursor.execute('SELECT status FROM subjects WHERE user_id = ? AND subject = ?', (user_id, subject))
        current_state = cursor.fetchone()[0]
        new_state = not current_state
        cursor.execute('UPDATE subjects SET status = ? WHERE user_id = ? AND subject = ?',
                       (new_state, user_id, subject))
        conn.commit()
        return new_state
    finally:
        conn.close()
