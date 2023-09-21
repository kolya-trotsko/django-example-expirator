import sqlite3
from setting.config import DB_PATH


def get_godaddy_acc():
    with sqlite3.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT api_key, api_secret, owner FROM godaddies")
        rows = cur.fetchall()

    results = [dict(row) for row in rows]

    return results


def get_namecheap_acc():
    with sqlite3.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT api_key, api_user, client_ip FROM namecheaps")
        rows = cur.fetchall()

    results = [dict(row) for row in rows]

    return results


def get_ukraine_acc():
    with sqlite3.connect(DB_PATH) as db:
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT api_key, owner FROM ukraines")
        rows = cur.fetchall()

    results = [dict(row) for row in rows]

    return results
