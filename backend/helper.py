import sqlite3
from setting.config import DB_PATH


def deleted():
    with sqlite3.connect(DB_PATH) as db:
        cur = db.cursor()
        cur.execute("DELETE FROM dashboard_domain")
        cur.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = \"dashboard_domain\"")
        db.commit()


def add_new_column():
    with sqlite3.connect(DB_PATH) as db:
        cur = db.cursor()
        cur.execute("ALTER TABLE dashboard_domain ADD COLUMN ")
        db.commit()


def remove_column():
    with sqlite3.connect(DB_PATH) as db:
        cur = db.cursor()
        cur.execute("ALTER TABLE dashboard_domain DROP COLUMN ")
        db.commit()
