import traceback
import logging
from data.db.get_db_domains import get_db_domains_daily_check_whois_trouble
from data.db.update_db_domain import update_db_whois, update_db_domain_daily_check_whois_trouble
from data.get_data_about_domain_name.whois.get_whois import get_whois


def _update_whois(domains):
    for domain in domains:
        try:
            whois = get_whois(domain[0])
            update_db_whois({
                "domain": domain[0],
                "expiration_date": whois['expiration_date'],
                "name_servers": whois['name_servers'],
                "registrar": whois['registrar']
            })
        except Exception as e:
            error_text = "Error: {}\n{}".format(str(e), traceback.format_exc())
            logging.error(error_text)
            

def daily_check_whois_trouble():
    update_db_domain_daily_check_whois_trouble()
    domains = get_db_domains_daily_check_whois_trouble()

    _update_whois(domains)
