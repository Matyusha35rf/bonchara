import config
from re import search

def get_id_zan(session):
    """
    Получение id открытого занятия
    :param session:
    :return: id открытого занятия
    """
    rasp = session.get(
        config.target_url,
        headers=config.headers
    ).text

    match_id = search(r'open_zan\((\d+),', rasp)
    id_zan = int(match_id.group(1)) if match_id else None

    match_week = search(rf'open_zan\({id_zan},(\d+)', rasp)
    week_zan = int(match_week.group(1)) if match_week else None
    return id_zan, week_zan

def visiting(session):
    """
    Нажатие на кнопку занятия
    :param session:
    :return: True - кнопка была нажата, False - занятие открыто, но кнопка не нажата, None - произошла ошибка
    """
    try:
        id_zan, week_zan = get_id_zan(session)
        if id_zan is None or week_zan is None:
            return False, "Нет открытых занятий"
        else:
            print(id_zan, week_zan)
            params = {"open": 1, "rasp": int(id_zan), "week": int(week_zan)}
        target_response = session.get(
            config.target_url,
            params=params,
            headers=config.headers
        )
        if target_response.status_code == 200:
            print(target_response.status_code, target_response.text)
            return True, "Отмечен"
        return False, target_response.text
    except Exception as e:
        print(e)
        return None, "Ошибка при отметке"
