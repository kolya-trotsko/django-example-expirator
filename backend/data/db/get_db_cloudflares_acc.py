import sqlite3
from setting.config import DB_PATH


def get_cloudflare_acc():
    with sqlite3.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT key, email FROM cloudflares")
        rows = cur.fetchall()

    results = [dict(row) for row in rows]

    return results
