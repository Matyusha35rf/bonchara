from lk.parsing_schedule import parse_schedule
from lk.match_groups import find_id_by_name


def format_dict(group, week):
    schedule_dict, days_list = parse_schedule(group, week)
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


def get_schedule_by_id(id_group, week):
    return format_dict(id_group, week)


def get_schedule_by_name(name_group, week):
    id_group = find_id_by_name(name_group)
    if id_group is None:
        return None
    schedule = get_schedule_by_id(id_group, week)
    return schedule


def get_schedule_current_day_by_id(id_group, week, day_week):
    schedule = get_schedule_by_id(id_group, week)
    if schedule is None:
        return None
    for day in schedule:
        if day.day_week.lower() == day_week.lower():
            return schedule[day]


def get_schedule_current_day_by_name(name_group, week, day_week):
    id_group = find_id_by_name(name_group)
    schedule = get_schedule_by_id(id_group, week)
    if id_group is None:
        return None
    for day in schedule:
        if day.day_week.lower() == day_week.lower():
            return schedule[day]



if __name__ == '__main__':
    schedule = get_schedule_by_name('ИСТ-341', 8)
    day_schedule = get_schedule_current_day_by_name('ИСТ-341', week=0, day_week='среда')
    print(day_schedule)
