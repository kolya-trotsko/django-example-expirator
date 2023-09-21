import datetime
import sqlite3
from setting.config import DB_PATH


def daily_check_days_left():
    with sqlite3.connect(DB_PATH) as db:
        cur = db.cursor()
        current_date = datetime.datetime.now()
        cur.execute("UPDATE dashboard_domain SET days_left = "
                    "CASE "
                    "WHEN last_expiration_date IS NULL THEN NULL "  
                    "ELSE CAST(julianday(last_expiration_date) - julianday(?) AS INTEGER) "
                    "END", (current_date,))
        db.commit()
