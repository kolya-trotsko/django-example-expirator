import sqlite3
from setting.config import DB_PATH


def get_db_binoms():
    with sqlite3.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT * FROM binoms")
        rows = cur.fetchall()

    binoms = []
    for row in rows:
        binom = dict(row)
        binoms.append(binom)

    return binoms


def get_db_binom(binom_name):
    with sqlite3.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT * FROM binoms WHERE binom = ?", (binom_name,))
        row = cur.fetchone()

    binom_dict = dict(row) if row else None

    return binom_dict
