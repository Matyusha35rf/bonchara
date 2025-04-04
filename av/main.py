import asyncio
import datetime
import datetime as dt
import os
import sys
import time
import sqlite3

from av.auto_visit import System
from bot.send import send_message


class App:
    def __init__(self):
        self.system = System()

    def read_db(self, filename):
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        return conn, cursor

    def get_users(self, cursor):
        src = cursor.execute("SELECT * FROM users").fetchall()
        headers = [i[1] for i in cursor.execute("PRAGMA table_info(users)").fetchall()]
        users = [dict(zip(headers, row)) for row in src]
        return users

    def marked_off(self, con, cur, now):
        print(f"Отметки сброшены в {now}")
        cur.execute(
            f'''UPDATE users
                SET marked = 0''')
        con.commit()

    def marked_on(self, con, cur, user_id):
        cur.execute(
            f'''UPDATE users
             SET marked = 1
             WHERE user_id = {user_id}''')
        con.commit()

    def run(self, filename):

        con, cur = self.read_db(filename)
        users = self.get_users(con)
        time_now = dt.datetime.now().strftime("%H:%M")
        if time_now in ["08:50", "10:35", "12:20", "14:35", "16:20", "18:05"]:
            self.marked_off(con, cur, time_now)
            time.sleep(30)
        else:
            for user in users:
                if user['sub'] and user['is_available'] and not user['marked']:
                    status, mes = self.system.run(user["e_mail"], user["password"])
                    if status:
                        self.marked_on(con, cur, user['user_id'])
        con.close()


if __name__ == "__main__":
    app = App()
    db_path = 'data/users.db'
    start = time.time()
    con, cur = app.read_db(db_path)
    app.marked_off(con, cur, 'Стартовая')
    print(f'{start} Автопосещение начал работу')
    while True:
        app.run(db_path)
        time.sleep(15)
    # finish = time.time()
    # print(finish - start)
