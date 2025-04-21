import datetime

from app_functions.schedule import schedule, work_with_data
from data import database
from datetime import datetime, timedelta
import config


def schedule_message_templates(user_id, mode, offset):
    result = ""
    user_group = database.get_user(user_id)["user_group"]
    if mode == "day":
        day_number = (datetime.today() + timedelta(days=offset)).weekday()
        lessons = schedule.get_schedule_current_day_by_name('rel', user_group, day_number)
        data = work_with_data.get_russian_date() + "\n"
        data += str(work_with_data.get_current_semester_week(config.start_first_sem)) + " неделя"
        result = data + "\n\n\n"

        for lesson in lessons:
            if lesson.title is not None:
                # Формируем строку времени
                time_str = ""
                if lesson.lesson_num is not None:
                    time_str = (
                        f"<b>{str(lesson.lesson_num.start_time).lstrip('0')}–"
                        f"{str(lesson.lesson_num.end_time).lstrip('0')}</b>\n"
                        f"<b>{lesson.lesson_num.lesson_num}.</b> "
                    )

                # Основная информация
                lesson_str = f"{time_str}<b>{lesson.title}</b>"

                # Тип занятия на новой строке
                if lesson.lesson_type:
                    lesson_str += f"\n<i>{lesson.lesson_type}</i>"

                # Преподаватель и аудитория
                details = []
                if lesson.teacher:
                    details.append(lesson.teacher)
                if lesson.auditorium:
                    aud = str(lesson.auditorium).replace("ауд.: ", "").replace("; Б22/2", "/2").replace(
                        "; Б22/1", "/1")
                    details.append(f"<b>{aud}</b>")

                if details:
                    lesson_str += "\n" + " | ".join(details)

                result += lesson_str + "\n\n"
    elif mode == "week":
        week_num = work_with_data.get_current_semester_week(config.start_first_sem)
        week = schedule.get_schedule_by_name('abs', user_group, week_num)
        data = str(week_num) + " неделя"
        result = data + "\n\n"

        for day in week:
            if day.day_week is not None:
                # Заголовок дня недели
                result += f"\n<b>━━ {day} ━━</b>\n\n"

                lessons = week[day]
                for lesson in lessons:
                    if not lesson.title:
                        continue

                    # Форматирование времени и номера пары
                    time_str = ""
                    if lesson.lesson_num:
                        time_str = (
                            f"{lesson.lesson_num.start_time.lstrip('0')}–"
                            f"{lesson.lesson_num.end_time.lstrip('0')}\n"
                            f"{lesson.lesson_num.lesson_num}. "
                        )

                    # Название предмета на новой строке
                    lesson_str = f"{time_str}<b>{lesson.title}</b>"

                    # Тип занятия на новой строке
                    if lesson.lesson_type:
                        lesson_str += f"\n<i>{lesson.lesson_type}</i>"

                    # Преподаватель и аудитория
                    details = []
                    if lesson.teacher:
                        details.append(lesson.teacher)
                    if lesson.auditorium:
                        aud = str(lesson.auditorium).replace("ауд.: ", "").replace("; Б22/2", "/2").replace(
                            "; Б22/1", "/1")
                        details.append(f"<b>{aud}</b>")

                    if details:
                        lesson_str += "\n" + " | ".join(details)

                    result += lesson_str + "\n\n"
    return result
