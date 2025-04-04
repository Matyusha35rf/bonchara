import os
import sqlite3
import sys
import logging

import requests

from bot.send import send_message
import config
from lk.lk_func import auth
from lk.av_func import visiting

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("av_logs.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('auto_visit')


class System:
    def check_correct_requests(self, var, mes, section):
        """Проверяет ответ запроса и логирует результат."""
        if var:
            logger.info(f"{section}: Успешно")
        elif var is False:
            logger.warning(f"{section}: {mes}")
        elif var is None:
            logger.error(f"{section}: {mes}")
            send_message(876644243, f'{section}: {mes}')
            # Вместо полного завершения работы, можно выбросить исключение
            raise Exception(f"Критическая ошибка в {section}: {mes}")

    def run(self, email, password):
        """Выполняет вход и отметку."""
        try:
            with requests.Session() as session:
                sign_in, mes = auth(session, email, password)
                logger.info(mes)
                self.check_correct_requests(sign_in, mes, "Вход")

                visit, mes = visiting(session)
                logger.info(f"Отметка: {mes}")
                self.check_correct_requests(visit, mes, "Отметка")
            return visit, mes
        except Exception as e:
            logger.error(f"Ошибка при выполнении: {e}")
            return None, str(e)


if __name__ == "__main__":
    system = System()
    db_path = "data/users.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT e_mail, password FROM users')
        users = cursor.fetchall()
        conn.close()
        
        for email, password in users:
            try:
                result, message = system.run(email, password)
                logger.info(f"Результат для {email}: {message}")
            except Exception as e:
                logger.error(f"Ошибка для пользователя {email}: {e}")
    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}")
        send_message(876644243, f'Критическая ошибка: {e}')

