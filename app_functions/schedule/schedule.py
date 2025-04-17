from pprint import pprint

from lk.parsing_schedule import parse_schedule
from lk.match_groups import find_id_by_name


def format_dict(mode, group, week):
    schedule_dict, days_list = parse_schedule(mode, group, week)
    if not days_list or not schedule_dict:
        return None
    formated_schedule = {}
    for lesson_row in schedule_dict:
        for lesson in lesson_row:
            for day in range(len(days_list)):
                if days_list[day] not in formated_schedule:
                    formated_schedule[days_list[day]] = [lesson_row[lesson][day]]
                else:
                    formated_schedule[days_list[day]].append(lesson_row[lesson][day])
    return formated_schedule


def get_schedule_by_id(mode, id_group, week):
    schedule = format_dict(mode, id_group, week)
    return schedule


def get_schedule_by_name(mode, name_group, week):
    id_group = find_id_by_name(name_group)
    if id_group is None:
        return None
    schedule = get_schedule_by_id(mode, id_group, week)
    return schedule


def get_schedule_current_day_by_id(mode, id_group, week, day_week):
    schedule = get_schedule_by_id(mode, id_group, week)
    if schedule is None:
        return None
    for day in schedule:
        if day.day_week.lower() == day_week.lower():
            return schedule[day]


def get_schedule_current_day_by_name(mode, name_group, day_week):
    id_group = find_id_by_name(name_group)
    print(id_group)
    schedule = get_schedule_by_id(mode, id_group, 0)
    if id_group is None:
        return None
    for day in schedule:
        if day.day_week.lower() == day_week.lower():
            return schedule[day]


def write_db_schedule_current_day():
    from data.database import connect

    week_rus = {'Monday': 'Понедельник',
                'Tuesday': 'вторник',
                'Wednesday': 'среда',
                'Thursday': 'четверг',
                'Friday': 'пятница',
                'Saturday': 'суббота',
                'Sunday': 'воскресенье'
                }
    con, cur = connect()
    id_groups_set = set([data[0] for data in cur.execute("SELECT user_group FROM users").fetchall()])
    for group in id_groups_set:
        schedule = get_schedule_by_name('rel', group, 0)

        


if __name__ == '__main__':
    schedule = get_schedule_by_name('abs', 'ИСТ-341',1)
    pprint(schedule)
    # write_db_schedule_current_day()
