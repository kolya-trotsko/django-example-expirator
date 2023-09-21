import sqlite3
from setting.config import DB_PATH


def add_new_domain_to_database(dict):
	with sqlite3.connect(DB_PATH) as db:
		cur = db.cursor()

		cur.execute("INSERT INTO dashboard_domain (domain_name, last_expiration_date,\
			days_left, binom_allowed, binom_exists, name_servers, registrar, cloudflare_acc, ssl_days_left, days_clicks_60, \
			ssl_error, archived, check_whois, binom_owner, registrar_acc, cf_ns) \
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            dict.get('domain', None), 
                            dict.get('last_expiration_date', None),
                            dict.get('days_left', None), 
                            dict.get('binom_allowed', None),
                            dict.get('binom_exists', None),
                            dict.get('name_servers', None), 
                            dict.get('registrar', None),
                            dict.get('cloudflare_acc', None),
                            dict.get('ssl_days_left', None),
                            dict.get('days_clicks_60', None), 
                            dict.get('ssl_error', None),
                            dict.get('archived', False),
                            dict.get('check_whois', False),
                            dict.get('binom_owner', None),
                            dict.get('registrar_acc', None),
			                dict.get('cf_ns', False),
                            ))

		db.commit()
