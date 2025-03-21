import requests

import config
from data import payload

class Schedule:
    def __init__(self):
        pass

    def auth(self, session, email, password):
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
                return True, "Вход выполнен"
            else:
                return False, "Вход невыполнен"
        except Exception as e:
            print(e)
            return None, "Ошибка при входе"

    def showweek(self, session, val):
        url = "https://lk.sut.ru/cabinet//project/cabinet/forms/raspisanie.php"
        params = {"week": val}

        response = session.get(url, params=params, headers=config.headers)

        if response.status_code == 200:
            # Если запрос успешен, можно вывести содержимое страницы
            print(response.text)
        else:
            print(f"Ошибка: {response.status_code}")

        return 0, 0

    def run(self):
        with requests.Session() as session:
            sign_in, mes = self.auth(session, payload['users'], payload['parole'])
            print(mes)
            status, schedule = self.showweek(session, 28)


if __name__ == "__main__":
    schedule = Schedule()

    auth = schedule.run()


