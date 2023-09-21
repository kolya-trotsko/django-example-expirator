from setting.config import DB_PATH
import traceback
import logging
import sqlite3


def update_db_notifications(data_dict):
    try:
        domain = data_dict["domain"]
        del data_dict["domain"]

        with sqlite3.connect(DB_PATH) as db:
            cur = db.cursor()

            cur.execute("SELECT COUNT(*) FROM notifications WHERE domain = ?", (domain,))
            count = cur.fetchone()[0]

            if count > 0:
                update_query = "UPDATE notifications SET "
                update_values = [f"{key} = ?" for key in data_dict.keys()]
                update_query += ", ".join(update_values) + " WHERE domain = ?"
                cur.execute(update_query, tuple(data_dict.values()) + (domain,))
            else:
                keys_formatted = ', '.join([f'"{key}"' for key in data_dict.keys()])
                placeholders = ', '.join(['?' for _ in data_dict.keys()])
                insert_query = f"INSERT INTO notifications ({keys_formatted}, domain) VALUES ({placeholders}, ?)"
                cur.execute(insert_query, tuple(data_dict.values()) + (domain,))

            db.commit()

    except Exception as e:
        error_text = "Error: {}\n{}".format(str(e), traceback.format_exc())
        logging.error(error_text)
