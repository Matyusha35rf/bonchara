import re
import time
from datetime import datetime, date
from datetime import timedelta
from pprint import pprint

import config
from lk import lk_func

from selectolax.parser import HTMLParser


class Date:
    def __init__(self, date, day_week):
        self.date = date
        self.day_week = day_week

    def __str__(self):
        return f'{self.date} {self.day_week}'

    def __repr__(self):
        return f'{self.date} {self.day_week}'


class Lesson:
    def __init__(self, lesson_num, title, teacher, auditorium, lesson_type):
        self.lesson_num = lesson_num
        self.title = title
        self.teacher = teacher
        self.auditorium = auditorium
        self.lesson_type = lesson_type

    def __str__(self):
        return f'{self.lesson_num} {self.title} {self.teacher} {self.auditorium} {self.lesson_type}'

    def __repr__(self):
        return f'{self.lesson_num} {self.title} {self.teacher} {self.auditorium} {self.lesson_type}'


class LessonNum:
    def __init__(self):
        self.lesson_num = None
        self.start_time = None
        self.end_time = None

    def splitter(self, root):
        # Получаем номер урока
        lesson_num_node = root.css_first(".vt283")
        self.lesson_num = lesson_num_node.text() if lesson_num_node else None
        times = re.findall(r'>\s*(\d{2}:\d{2})\s*<', root.html)
        self.start_time = times[0] if len(times) > 0 else None
        self.end_time = times[1] if len(times) > 1 else None

        # Дополнительная валидация формата времени
        time_pattern = re.compile(r'^\d{2}:\d{2}$')
        if self.start_time and not time_pattern.match(self.start_time):
            self.start_time = None
        if self.end_time and not time_pattern.match(self.end_time):
            self.end_time = None

    def __str__(self):
        return f'{self.lesson_num} {self.start_time}-{self.end_time}'

    def __repr__(self):
        return f'{self.lesson_num} {self.start_time}-{self.end_time}'


def delta_date(date, week):
    #print(week)
    delta_week = timedelta(weeks=week)
    date += delta_week
    date = date.strftime('%Y-%m-%d')
    return date


def get_url(group, week):
    date = delta_date(datetime.today(), week)
    url = f"https://www.sut.ru/studentu/raspisanie/raspisanie-zanyatiy-studentov-ochnoy-i-vecherney-form-obucheniya?group={group}&date={date}"
    return url

def get_url_abs(id_group, week):
    target_date = delta_date(config.start_first_sem, week-1)
    print(target_date)
    url = f"https://www.sut.ru/studentu/raspisanie/raspisanie-zanyatiy-studentov-ochnoy-i-vecherney-form-obucheniya?group={id_group}&date={target_date}"
    return url


def get_days(tree):
    days_html = tree.css_first('.vt244a').css('.vt237')
    days_list = []
    for i in range(1, len(days_html)):
        day = days_html[i].text().strip().split()
        days_list.append(Date(day[0], day[1]))
    return days_list


def check_existing_css(css):
    if css is not None:
        return css.text().strip()


def get_rasp(tree):
    rows = tree.css_first('.vt244b').css('.vt244')
    rasp_days_list_formated = []
    for row in rows:
        rasp_day_list = row.css('.rasp-day')
        lesson_num_html = row.css_first('div.vt239')
        lesson_num = LessonNum()
        lesson_num.splitter(lesson_num_html)
        dict_day = {lesson_num: []}
        for j in rasp_day_list:
            title = check_existing_css(j.css_first('.vt240'))
            teacher = check_existing_css(j.css_first('.vt241'))
            auditorium = check_existing_css(j.css_first('.vt242'))
            type_lesson = check_existing_css(j.css_first('.vt243'))
            dict_day[lesson_num].append(Lesson(lesson_num, title, teacher, auditorium, type_lesson))
        rasp_days_list_formated.append(dict_day)
    return rasp_days_list_formated


def parse_schedule(mode, group, week) -> (dict, list):
    if mode == 'abs':
        html = lk_func.connect(get_url_abs(group, week))
    elif mode == 'rel':
        html = lk_func.connect(get_url(group, week))
    else:
        return 'Режим не определен', 'Режим не определен'
    tree = HTMLParser(html)
    table = tree.css_first('div.vt236')
    if not table:
        return None, None
    days_list = get_days(table)
    schedule_dict = get_rasp(table)

    return schedule_dict, days_list

if __name__ == '__main__':
    start_time = time.time()

    finish_time = time.time()
    # print(finish_time - start_time)
