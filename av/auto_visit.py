import os
import sqlite3

import requests
from re import search
# from time import time

import config



class System:
    @staticmethod
    def check_correct_requests(var, section):
        if var:
            print(f"{section}: Все ок")
        if not var:
            print(f"{section}: Ответ на запрос не 200")
        elif var is None:
            print(f"{section}: Какая-то ошибка")

    @staticmethod
    def get_id_zan(session):
        rasp = session.get(
            config.target_url,
            headers=config.headers
        ).text

        match_id = search(r'open_zan\((\d+),', rasp)
        id_zan = int(match_id.group(1)) if match_id else None

        match_week = search(rf'open_zan\({id_zan},(\d+)', rasp)
        week_zan = int(match_week.group(1)) if match_week else None
        return id_zan, week_zan

    @staticmethod
    def auto(session, email, password):
        try:
            session.get(config.base_url, headers=config.headers)
            # Авторизация
            payload = {
                'users': email,  # Замените на ваш логин
                'parole': password,  # Замените на ваш пароль
            }
            auth_response = session.post(
                config.login_url,
                data=payload,
                headers=config.headers,
                allow_redirects=False
            )
            if auth_response.status_code == 200 and auth_response.text == "1":
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return None

    def visiting(self, session):
        try:
            id_zan, week_zan = self.get_id_zan(session)
            if id_zan is None or week_zan is None:
                params = {"open": 1, "rasp": 0, "week": 0}
            else:
                params = {"open": 1, "rasp": int(id_zan), "week": int(week_zan)}
            target_response = session.get(
                config.target_url,
                params=params,
                headers=config.headers
            )
            if target_response.status_code == 200:
                print(target_response.status_code, target_response.text)
                return True
            return False
        except Exception as e:
            print(e)
            return None

    def run(self, email, password):
        with requests.Session() as session:
            sign_in = self.auto(session, email, password)
            self.check_correct_requests(sign_in, "Вход")

            visit = self.visiting(session)
            self.check_correct_requests(visit, "Отметка")


if __name__ == "__main__":

    system = System()
    db_path = os.path.join('..', 'data', 'users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT e_mail, password FROM users')
    users = cursor.fetchall()
    conn.close()
    while True:
        for email, password in users:
            system.run(email, password)
