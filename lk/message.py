import sys
from lk.lk_func import auth

import requests

import config

from selectolax.parser import HTMLParser


def tr_click(id, session):
    url = "https://lk.sut.ru/cabinet/project/cabinet/forms/sendto2.php"

    data = {
        "id": id,
        "prosmotr": ""
    }

    response = session.post(url, data=data, headers=config.headers)

    if response.status_code == 200:
        print("Запрос успешен!")
        try:
            json_data = response.json()
            print("Ответ сервера:", json_data)
        except ValueError:
            print("Ответ сервера (не JSON):", response.text)
    else:
        print("Ошибка запроса:", response.status_code)


def get_message_by_id(id_mes, email, password):
    with requests.Session() as session:
        status, mes = auth(session, email, password)
        tr_click(id_mes, session)


def get_id_last_message(email, password):
    with requests.Session() as session:
        # Авторизация
        status, mes = auth(session, email, password)
        if not status:
            return None

        # Шаг 1: Сначала запрашиваем главную страницу кабинета
        session.get(
            "https://lk.sut.ru/cabinet/",
            headers=config.headers
        )

        response = session.get(
            "https://lk.sut.ru/cabinet/project/cabinet/forms/message.php",
            headers=config.headers,
        )
        html = response.text
        tree = HTMLParser(html)
        table = tree.css_first('table.simple-little-table').css_first('tbody')
        last_mes = table.css_first('tr')
        last_mes_id = last_mes.attributes['id'].split('_')[1]
        return last_mes_id



if __name__ == '__main__':
    last_message_id = get_id_last_message('texin508@gmail.com', 'al20an05')
    print(f"ID последнего сообщения: {last_message_id}")
