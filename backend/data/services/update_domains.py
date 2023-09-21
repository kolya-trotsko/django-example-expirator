import traceback
import logging

from data.db.get_db_domains import get_old_db_domains_list
from data.db.add_new_domain_to_database import add_new_domain_to_database
from data.db.update_db_domain import update_db_domain

from data.services.binom.get_binom_domains import get_binom_domains
from data.services.cloudflare.domains.get_cloudflare_domains import get_cloudflare_domains
from data.services.registrar.get_godaddy_domains import get_godaddy_domains
from data.services.registrar.get_namecheap_domains import get_namecheap_domains

from data.get_data_about_domain_name.get_data_about_domain_name import get_domain_name_data
from notification.telegram_notification import send_telegram_notification


def _get_domains_dict(func):
    domains = {}
    try:
        func_domains = func()
        for domain in func_domains:
            if domain in domains:
                domains[domain].update(func_domains[domain])
            else:
                domains[domain] = func_domains[domain]

    except Exception as e:
        error_text = "Error: {}\n{}".format(str(e), traceback.format_exc())
        logging.error(error_text)
        send_telegram_notification(text=f"update_domains_get_domains_dict, {str(e)}")

    return domains


def _update_domains_dict(domains):
    for domain in domains:
        try:
            domains[domain]["domain"] = domain
            data = get_domain_name_data(domain, domains[domain])
            if data is not None:
                domains[domain].update(data)
        except Exception as e:
            error_text = "Error: {}\n{}".format(str(e), traceback.format_exc())
            logging.error(error_text)
            send_telegram_notification(text=f"update_domains_update_domains_dict, {str(e)}")

    return domains


def _add_or_update_domains(domains):
    old_domains_list = get_old_db_domains_list()
    for domain in domains:
        try:
            if domain in old_domains_list:
                update_db_domain(domains[domain])
            else:
                add_new_domain_to_database(domains[domain])

        except Exception as e:
            error_text = "Error: {}\n{}".format(str(e), traceback.format_exc())
            logging.error(error_text)
            send_telegram_notification(text=f"update_domains_add_or_update_domains, {str(e)}")


def update_domains():
    for func in [get_binom_domains, get_godaddy_domains, get_namecheap_domains, get_cloudflare_domains]:
        try:
            domains = _get_domains_dict(func)
            domains = _update_domains_dict(domains)
            _add_or_update_domains(domains)

        except Exception as e:
            error_text = "Error: {}\n{}".format(str(e), traceback.format_exc())
            logging.error(error_text)
            send_telegram_notification(text=f"update_domains, {str(e)}")
