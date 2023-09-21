from data.get_data_about_domain_name.ssl_error.get_ssl_error import get_ssl_error
from data.db.update_db_domain import update_db_domain
from data.db.get_db_domains import get_db_domains
import logging
import traceback


def daily_check_ssl_error():
    domains = get_db_domains()

    for domain in domains:
        try:
            ssl_error = get_ssl_error(domain["domain_name"])
            if domain["ssl_error"] != ssl_error:
                update_db_domain({
                    "domain": domain["domain_name"],
                    "ssl_error": ssl_error
                })

        except Exception as e:
            error_text = "Error: {}\n{}".format(str(e), traceback.format_exc())
            logging.error(error_text)
