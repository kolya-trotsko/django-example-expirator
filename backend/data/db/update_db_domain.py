from setting.config import DB_PATH
import sqlite3
import traceback
import logging


def update_db_domain(data_dict):
    try:
        domain = data_dict["domain"]
        del data_dict["domain"]

        with sqlite3.connect(DB_PATH) as db:
            cur = db.cursor()

            update_query = "UPDATE dashboard_domain SET "
            update_values = []
            for key, value in data_dict.items():
                if isinstance(value, list):
                    if value:
                        value = ", ".join(map(str, value))
                    else:
                        value = ""
                elif value == "" or value == [] or value == {}:
                    value = None

                update_query += "{} = ?, ".format(key)
                update_values.append(value)
            update_query = update_query.rstrip(", ")
            update_query += " WHERE domain_name = ?"
            update_values.append(domain)

            cur.execute(update_query, tuple(update_values))
            db.commit()

    except Exception as e:
        error_text = "Error: {}\n{}".format(str(e), traceback.format_exc()) + f"data_dict: {data_dict}"
        logging.error(error_text)


def update_db_whois(data_dict):
    domain = data_dict["domain"]
    del data_dict["domain"]

    with sqlite3.connect(DB_PATH) as db:
        cur = db.cursor()
        cur.execute("PRAGMA table_info(dashboard_domain)")
        columns = [column[1] for column in cur.fetchall() if column[1] != "id"]

        set_clause = ", ".join([f"{column} = COALESCE(?, {column})" for column in columns])
        params = [data_dict.get(column, None) for column in columns]
        params.append(domain)
        where_clause = "WHERE domain_name = ?"
        cur.execute(f"UPDATE dashboard_domain SET {set_clause} {where_clause}", tuple(params))
        db.commit()


def update_db_domain_daily_check_whois_trouble():
    with sqlite3.connect(DB_PATH) as db:
        cur = db.cursor()
        cur.execute("UPDATE dashboard_domain SET check_whois = COALESCE(check_whois, 0) + 1 \
                    WHERE \"days_left\" IS NULL OR \"last_expiration_date\" IS NULL OR \
                    \"ssl_days_left\" IS NULL")
        db.commit()
