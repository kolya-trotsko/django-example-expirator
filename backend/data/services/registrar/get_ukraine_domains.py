from data.get_data_about_domain_name.binom_allowed.get_binom_allowed import get_binom_allowed
from data.db.get_db_domains import get_db_domains
from data.db.update_db_domain import update_db_domain
import traceback
import logging


def daily_check_binom_allowed():
    domains = get_db_domains()
    for domain in domains:
        try:
            binom_allowed = get_binom_allowed(domain["domain_name"])
            if domain["binom_allowed"] != binom_allowed:
                update_db_domain({
                    "domain": domain["domain_name"],
                    "binom_allowed": binom_allowed
                })

        except Exception as e:
            error_text = "Error: {}\n{}".format(str(e), traceback.format_exc())
            logging.error(error_text)
