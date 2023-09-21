import sqlite3
from setting.config import DB_PATH


def get_db_notifications():
    with sqlite3.connect(DB_PATH) as db:
        cur = db.cursor()
        cur.execute('SELECT * FROM notifications')

        columns = [description[0] for description in cur.description]
        data_db = cur.fetchall()

        data = {}
        for row in data_db:
            domain_data = dict(zip(columns, row))
            domain = domain_data["domain"]
            del domain_data["domain"]
            data[domain] = domain_data

        return data
