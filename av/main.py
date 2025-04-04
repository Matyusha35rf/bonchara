import asyncio
import datetime
import datetime as dt
import os
import sys
import time
import sqlite3

from av.auto_visit import System
from bot.send import send_message
from data.database import read_db, get_users, marked_on, marked_off


class App:
    def __init__(self):
        self.system = System()

    def run(self, filename):
        con, cur = read_db(filename)
        users = get_users(con)
        time_now = dt.datetime.now().strftime("%H:%M")
        if time_now in ["08:50", "10:35", "12:20", "14:35", "16:20", "18:05"]:
            marked_off(con, cur, time_now)
            time.sleep(30)
        else:
            for user in users:
                if user['sub'] and user['is_available'] and not user['marked']:
                    status, mes = self.system.run(user["e_mail"], user["password"])
                    if status:
                        marked_on(con, cur, user['user_id'])
        con.close()


if __name__ == "__main__":
    app = App()
    db_path = 'data/users.db'
    start = time.time()
    con, cur = read_db(db_path)
    marked_off(con, cur, 'Стартовая')
    print(f'{start} Автопосещение начал работу')
    while True:
        app.run(db_path)
        time.sleep(15)
    # finish = time.time()
    # print(finish - start)
