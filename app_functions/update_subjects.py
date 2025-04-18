from app_functions.schedule.schedule import get_schedule_by_name
from data import database


async def update_subjects(user_id):
    try:
        user_id = int(user_id)
        subjects_old = set(database.get_subjects_status(user_id).keys())
        group_name = database.get_user(user_id)["user_group"]
        subjects_new = []
        for week in range(1, 18):
            schedule = get_schedule_by_name("abs", group_name, week)
            for i in schedule:
                for j in schedule[i]:
                    title = j.title
                    if title is not None:
                        subjects_new.append(j.title)
        subjects_new = set(subjects_new)
        if len(subjects_new) > 0:
            subjects_del = subjects_old - subjects_new
            subjects_add = subjects_new - subjects_old
            database.del_subjects(user_id, subjects_del)
            database.add_to_db_subjects(user_id, subjects_add)

    except Exception as e:
        print(f"Ошибка в обновлении предметов:{e}")


if __name__ == "__main__":
    update_subjects("ИСТ-341")
