import sqlite3
from setting.config import DB_PATH


def get_old_db_domains_list():
    with sqlite3.connect(DB_PATH) as db:
        cur = db.cursor()
        cur.execute('SELECT domain_name FROM dashboard_domain')
        rows = cur.fetchall()
        domains = [row[0] for row in rows]

        return domains


def get_db_domains():
    with sqlite3.connect(DB_PATH) as db:
        cur = db.cursor()
        cur.execute('SELECT * FROM dashboard_domain')

        columns = [description[0] for description in cur.description]
        dataDB = cur.fetchall()

        domains = []
        for row in dataDB:
            domain_data = dict(zip(columns, row))
            domains.append(domain_data)

        return domains


def get_db_domains_daysleft_notification():
    with sqlite3.connect(DB_PATH) as db:
        cur = db.cursor()
        query = f"SELECT * FROM dashboard_domain WHERE days_left > 0 AND days_left <= 10 AND archived = 0"
        dataDB = cur.execute(query).fetchall()

        columns = [description[0] for description in cur.description]

        result = []
        for row in dataDB:
            domain_data = dict(zip(columns, row))
            result.append(domain_data)

        return result


def get_db_domains_daily_check_whois_trouble():
    with sqlite3.connect(DB_PATH) as db:
        cur = db.cursor()
        domains = cur.execute("SELECT domain_name FROM dashboard_domain WHERE \
                              (\"days_left\" IS NULL OR \"last_expiration_date\" IS NULL) AND \
                               (\"check_whois\" < 5 OR \"check_whois\" % 5 = 0)").fetchall()

        return domains


