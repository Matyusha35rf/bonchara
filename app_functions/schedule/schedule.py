import requests

import config
from app_functions.schedule.data import payload

from lk.lk_func import auth


class Schedule:
    def __init__(self):
        pass

    def showweek(self, session):
        url = "https://lk.sut.ru/cabinet//project/cabinet/forms/raspisanie.php"
        # params = {"week": }

        response = session.get(url,  headers=config.headers)

        if response.status_code == 200:
            # Если запрос успешен, можно вывести содержимое страницы
            print(response.text)
        else:
            print(f"Ошибка: {response.status_code}")

        return 0, 0

    def run(self):
        with requests.Session() as session:
            sign_in, mes = auth(session, payload['users'], payload['parole'])
            print(mes)
            status, schedule = self.showweek(session)


if __name__ == "__main__":
    schedule = Schedule()
    auth = schedule.run()



