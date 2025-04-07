from pprint import pprint

from config import schedule_url
from lk.parsing_schedule import parse_schedule
from lk.match_groups import find_id_by_name


def format_dict(group, week):
    schedule_dict, days_list = parse_schedule(group, week)
    formated_schedule = {}
    print(days_list)
    for lesson_row in schedule_dict:
        for lesson in lesson_row:
            for day in range(len(days_list)):
                if days_list[day] not in formated_schedule:
                    formated_schedule[days_list[day]] = [[lesson, lesson_row[lesson][day]]]
                else:
                    formated_schedule[days_list[day]].append([lesson, lesson_row[lesson][day]])
    return formated_schedule


def get_schedule_by_id(id_group, week):
    return format_dict(id_group, week)


def get_schedule_by_name(name_group, week):
    id_group = find_id_by_name(name_group)
    if id_group is None:
        return None
    schedule = get_schedule_by_id(id_group, week)
    return schedule


if __name__ == '__main__':
    schedule = get_schedule_by_name('122А-24', 2)
    pprint(schedule)
