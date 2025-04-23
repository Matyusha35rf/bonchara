from datetime import datetime

import config
import requests


def auth(session, email, password):
    """
    Вход в личный кабинет
    :param session:
    :param email:
    :param password:
    :return: True - вход был успешно выполнен, False - вход не был выполнен, None - произошла ошибка
    """
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
            return False, "Вход не выполнен"
    except Exception as e:
        return None, str(e)


def connect(url):
    with requests.session() as session:
        response = session.get(url, headers=config.headers)
        if response.status_code == 200:
            return response.text
        else:
            print(response.status_code)


def connect_session(url, session):
    with session:
        response = session.get(url, headers=config.headers)
        if response.status_code == 200:
            return response.text
        else:
            print(response.status_code)


def get_number_lesson(time, mode='regular'):
    if mode == 'regular':
        time_arr = config.start_lessons
    elif mode == 'marking':
        time_arr = config.marking_time
    else:
        return -1
    for i in range(len(time_arr)):
        if datetime.strptime(time_arr[i], '%H:%M').time() <= datetime.strptime(time, '%H:%M').time() <= datetime.strptime(
            config.end_lessons[i], '%H:%M').time():
            return i+1
    return -1



