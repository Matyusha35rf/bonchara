import config

def auth(session, email, password):
    """
    Вход в личный кабинет
    :param session:
    :param email:
    :param password:
    :return: True - вход был успешно выполнен, False - вход не был выполнен, None - произошла ошибка
    """
    try:
        # a = 5/0
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

