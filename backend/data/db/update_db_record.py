import sqlite3
from setting.config import DB_PATH


def update_dns_record(record):
    with sqlite3.connect(DB_PATH) as db:
        cur = db.cursor()
        cur.execute(f"SELECT EXISTS(SELECT 1 FROM DNS_Records WHERE record_id = ? AND zone_id = ? AND domain = ?)", (record['id'], record['zone_id'], record['zone_name']))
        record_exists = cur.fetchone()[0]
        if record_exists:
            cur.execute(f"UPDATE DNS_Records SET domain = ?, type = ?, content = ?, proxied = ?, cf_email = ?, record_id = ?, zone_id = ? WHERE record_id = ? AND zone_id = ? AND domain = ?", (record['zone_name'], record['type'], record['content'], record['proxied'], record['cf_email'], record['id'], record['zone_id'], record['id'], record['zone_id'], record['zone_name']))
        else:
            cur.execute(f"INSERT INTO DNS_Records (domain, type, content, proxied, cf_email, record_id, zone_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (record['zone_name'], record['type'], record['content'], record['proxied'], record['cf_email'], record['id'], record['zone_id']))

        db.commit()
