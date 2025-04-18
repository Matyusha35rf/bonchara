import sqlite3
from datetime import datetime

from sqlite3.dbapi2 import sqlite_version_info

import config
from config import start_lessons, end_lessons


def get_users_notifications(time):
    from data.database import connect
    con, cur = connect()
    column = 'minutes_' + str(time)
    try:
        user_list = [i[0] for i in cur.execute(f'''SELECT user_id FROM notifications WHERE {column}=1''').fetchall()]
        return user_list
    except sqlite3.OperationalError:
        return []
    finally:
        con.close()


def set_bool_notifications(user_id, time):
    from data.database import connect
    con, cur = connect()
    column = 'minutes_' + str(time)
    try:
        cur.execute(f'''UPDATE notifications SET {column}=1 WHERE user_id=?''', (user_id, ))
        con.commit()
        return True
    except sqlite3.OperationalError:
        return False
    finally:
        con.close()

def reset_bool_notifications(user_id):
    from data.database import connect
    con, cur = connect()
    try:



if __name__ == '__main__':
    print(set_bool_notifications(876644243, 20))
