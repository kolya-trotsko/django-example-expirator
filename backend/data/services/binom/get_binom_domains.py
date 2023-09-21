import traceback
import logging
import time
from data.services.binom.get_binom_response import get_binom_response
from data.db.get_db_binoms import get_db_binoms


def get_binom_domains():
    domains = {}
    binoms = get_db_binoms()
    for binom in binoms:
        try:
            domains_res = get_binom_response(binom=binom,
                                             form=f"?page=Domains")
            for domain in domains_res:
                if domain['name'] in domains:
                    domains[domain['name']]['binom_exists'] += ", "+binom["binom"]
                    domains[domain['name']]['binom_exists'] += ", "+binom["owner"]
                else:
                    domains[domain['name']] = {"binom_exists": binom["binom"], 'binom_owner': binom["owner"]}
        except Exception as e:
            error_text = "Error: {}\n{}".format(str(e), traceback.format_exc())
            logging.error(error_text)
            time.sleep(2)

    return domains
