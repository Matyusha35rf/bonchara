import time
from datetime import datetime
from datetime import timedelta
from pprint import pprint

import lk_func

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
    def __init__(self, title, teacher, auditorium, lesson_type):
        self.title = title
        self.teacher = teacher
        self.auditorium = auditorium
        self.lesson_type = lesson_type

    def __str__(self):
        return f'{self.title} {self.teacher} {self.auditorium} {self.lesson_type}'

    def __repr__(self):
        return f'{self.title} {self.teacher} {self.auditorium} {self.lesson_type}'

class LessonNum:
    def __init__(self, lesson_num, start, end):
        self.lesson_num = lesson_num
        self.start = start
        self.end = end

    def __str__(self):
        return f'{self.lesson_num} {self.start}:{self.end}'

    def __repr__(self):
        return f'{self.lesson_num} {self.start}:{self.end}'


def get_url(group=56206, week=0):
    date = datetime.today()
    delta_week = timedelta(weeks=week)
    date += delta_week
    date = date.strftime('%Y-%m-%d')
    url = f"https://www.sut.ru/studentu/raspisanie/raspisanie-zanyatiy-studentov-ochnoy-i-vecherney-form-obucheniya?group={group}&date={date}"
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
    for i in rows:
        rasp_day_list = i.css('.rasp-day')
        lesson_num_html = i.css_first('.vt239')
        lesson_num_cnt = lesson_num_html.css_first('.vt283')
        start_end = lesson_num_html.css('br')
        lesson_num = LessonNum(check_existing_css(lesson_num_cnt),check_existing_css(start_end[0]),check_existing_css(start_end[1]))
        print(lesson_num)
        dict_day = {lesson_num: []}
        for j in rasp_day_list:
            title = check_existing_css(j.css_first('.vt240'))
            teacher = check_existing_css(j.css_first('.vt241'))
            auditorium = check_existing_css(j.css_first('.vt242'))
            type_lesson = check_existing_css(j.css_first('.vt243'))
            dict_day[lesson_num].append(Lesson(title, teacher, auditorium, type_lesson))
        rasp_days_list_formated.append(dict_day)
    return rasp_days_list_formated


def parse_schedule():
    html = lk_func.connect(get_url())
    tree = HTMLParser(html)
    table = tree.css_first('div.vt236')
    days_list = get_days(table)
    schedule_dict = get_rasp(table)

    return schedule_dict, days_list


def format_dict():
    schedule_dict, days_list = parse_schedule()
    formated_schedule = {}
    print(days_list)
    for lesson_row in schedule_dict:
        for lesson in lesson_row:
            for day in range(len(days_list)):
                if days_list[day] not in formated_schedule:
                    formated_schedule[days_list[day]] = [[lesson, lesson_row[lesson][day]]]
                else:
                    formated_schedule[days_list[day]].append([lesson, lesson_row[lesson][day]])
    pprint(formated_schedule)


if __name__ == '__main__':
    start_time = time.time()
    format_dict()
    finish_time = time.time()
    # print(finish_time - start_time)
