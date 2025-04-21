from datetime import date


from datetime import datetime, timedelta


def get_russian_date(offset=0):
    weekdays = {0: "Понедельник", 1: "Вторник", 2: "Среда", 3: "Четверг",
                4: "Пятница", 5: "Суббота", 6: "Воскресенье"}

    months = {1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая",
              6: "июня", 7: "июля", 8: "августа", 9: "сентября",
              10: "октября", 11: "ноября", 12: "декабря"}

    target_date = datetime.now() + timedelta(days=offset)
    return f"{weekdays[target_date.weekday()]}, {target_date.day} {months[target_date.month]} {target_date.year}"


def get_current_semester_week(start_date: date, current_date: date = None) -> int:
    """
    Вычисляет текущую неделю семестра.

    :param start_date: Дата начала семестра (1 неделя)
    :param current_date: Текущая дата (по умолчанию сегодня)
    :return: Номер текущей недели (начиная с 1)
    """
    if current_date is None:
        current_date = date.today()

    # Вычисляем разницу в днях
    delta = current_date - start_date

    # Вычисляем номер недели: делим на 7 дней и округляем вверх
    week_number = (delta.days // 7) + 1

    # Не может быть недели < 1
    return max(1, week_number)


# Пример использования
start_first_sem = datetime.strptime('10.02.2025', '%d.%m.%Y').date()
current_week = get_current_semester_week(start_first_sem)
