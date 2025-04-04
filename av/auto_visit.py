import asyncio
import os
import sqlite3
import sys

import requests
from re import search
# from time import time

from bot.send import send_message
import config
from lk.lk_func import auth
from lk.av_func import visiting


class System:
    def check_correct_requests(self, var,mes, section):
        # if var:
        #     print(f"{section}: Все ок")
        # if not var:
        #     print(f"{section}: Ответ на запрос не 200")
        if var is None:
            send_message(876644243, f'{section}: {mes}')
            sys.exit()
            # print(f"{section}: Какая-то ошибка")

    def run(self, email, password):
        with requests.Session() as session:
            sign_in, mes = auth(session, email, password)
            print(mes)
            self.check_correct_requests(sign_in, mes, "Вход")

            visit, mes = visiting(session)
            # print(mes)
            # self.check_correct_requests(visit, "Отметка")
        return visit, mes


if __name__ == "__main__":
    system = System()
    db_path = "data/users.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT e_mail, password FROM users')
    users = cursor.fetchall()
    conn.close()
    for email, password in users:
        system.run(email, password)

