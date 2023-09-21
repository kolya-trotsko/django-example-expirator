from data.db.update_db_domain import update_db_domain
from data.db.get_db_domains import get_db_domains
import traceback
import logging


def daily_check_cf_ns():
    domains = get_db_domains()
    for domain in domains:
        try:
            if domain["name_servers"] is None:
                cf_ns = 0
            elif "cloudflare" in str(domain["name_servers"]):
                cf_ns = 1
            else:
                cf_ns = 0

            update_db_domain({
                "domain": domain["domain_name"],
                "cf_ns": cf_ns
            })

        except Exception as e:
            error_text = "Error: {}\n{}".format(str(e), traceback.format_exc()) + f"\ndomain = {domain}"
            logging.error(error_text)
