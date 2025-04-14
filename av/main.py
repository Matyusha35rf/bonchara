import datetime as dt
import time
import logging
from contextlib import contextmanager

from av.auto_visit import System
from bot.send import send_message
from data.database import connect, get_users, marked_on, marked_off
import config

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("av_main_logs.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('av_main')


class App:
    def __init__(self):
        self.system = System()
        self.con, self.cur = connect()
        # logger.info("Приложение инициализировано")

    def check_missed_reset_time(self, time_now, reset_times):
        """
        Проверяет, не попало ли время сброса в интервал времени обработки
        
        Args:
            time_now (str): Время начала обработки в формате "HH:MM"
            reset_times (list): Список времён сброса
            
        Returns:
            bool: True если был выполнен сброс, False в противном случае
        """
        # Получаем текущее время после обработки
        time_after = dt.datetime.now().strftime("%H:%M")

        # Проверка пропущенного времени сброса между началом и концом обработки
        start_time = dt.datetime.strptime(time_now, "%H:%M")
        end_time = dt.datetime.strptime(time_after, "%H:%M")

        # Ищем время сброса в интервале обработки
        for reset_time in reset_times:
            reset_dt = dt.datetime.strptime(reset_time, "%H:%M")
            if start_time < reset_dt <= end_time:
                logger.info(f"Найдено пропущенное время сброса: {reset_time}")
                marked_off(self.con, self.cur, reset_time)
                return True

        return False

    def run(self, db_path=None):
        """
        Основная функция проверки и отметки пользователей
        """
        try:
            # Получаем список пользователей
            users = get_users(self.cur)
            time_now = dt.datetime.now().strftime("%H:%M")

            # Проверяем, не время ли сбросить отметки
            reset_times = config.end_lessons
            if time_now in reset_times:
                # logger.info(f"Сброс отметок в {time_now}")
                marked_off(self.con, self.cur, time_now)
                return  # Завершаем выполнение после сброса отметок

            # Иначе проверяем каждого пользователя
            sub_users = [u for u in users if u['sub'] and u['av_status'] and not u['marked']]
            # logger.info(f"Проверка {len(sub_users)} пользователей с подпиской")

            for user in sub_users:
                try:
                    status, mes = self.system.run(user["email"], user["password"])
                    # logger.info(f"Пользователь {user['e_mail']}: {mes}")

                    if status:
                        marked_on(self.con, self.cur, user['user_id'])
                        # logger.info(f"Пользователь {user['e_mail']} отмечен")
                except Exception as e:
                    logger.error(f"Ошибка при обработке пользователя {user['e_mail']}: {e}")

            # Проверяем, не пропустили ли время сброса во время обработки
            self.check_missed_reset_time(time_now, reset_times)

        except Exception as e:
            logger.error(f"Ошибка при выполнении run: {e}")
        finally:
            pass

    def close(self):
        """Закрытие соединений и ресурсов"""
        if hasattr(self, 'con') and self.con:
            self.con.close()
            logger.info("Соединение с БД закрыто")


if __name__ == "__main__":
    app = App()
    db_path = 'data/users.db'
    start_time = time.time()

    try:
        # Инициализация и запуск основного цикла
        app.con, app.cur = connect()
        marked_off(app.con, app.cur, 'Стартовая')
        logger.info(f"Автопосещение начало работу в {dt.datetime.now()}")

        # Используем обработку исключений для корректного завершения при прерывании
        try:
            while True:
                app.run(db_path)
                time.sleep(15)  # Пауза между циклами
        except KeyboardInterrupt:
            app.con.close()
            logger.info("Программа остановлена пользователем")
        except Exception as e:
            logger.critical(f"Критическая ошибка: {e}")
            send_message(876644243, f'Критическая ошибка в main.py: {e}')
        finally:
            app.close()

    except Exception as e:
        logger.critical(f"Ошибка при запуске: {e}")
    finally:
        runtime = time.time() - start_time
        logger.info(f"Общее время работы: {runtime:.2f} сек")
