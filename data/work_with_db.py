import sqlite3
from database import connect

con, cur = connect()
cur.execute('ALTER TABLE users ADD COLUMN semester INT')
con.commit()
con.close()
