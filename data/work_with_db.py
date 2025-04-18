import sqlite3
from database import connect

con, cur = connect()
cur.execute('')
con.commit()
con.close()
