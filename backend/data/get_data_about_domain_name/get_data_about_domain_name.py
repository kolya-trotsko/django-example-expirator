import traceback
import logging
import datetime
from data.get_data_about_domain_name.whois.get_whois import get_whois
from data.get_data_about_domain_name.ssl_error.get_ssl_error import get_ssl_error
from data.get_data_about_domain_name.binom_allowed.get_binom_allowed import get_binom_allowed
from data.get_data_about_domain_name.ssl_days_left.get_days_left_ssl import get_ssl_days_left


def get_domain_name_data(domain, domain_dict):
    try:
        data = {}
        if 'last_expiration_date' not in domain_dict or 'name_servers' not in domain_dict or 'registrar' not in domain_dict:
            whois = get_whois(domain)

            if 'last_expiration_date' not in domain_dict:
                if whois['expiration_date'] is not None:
                    data['last_expiration_date'] = datetime.datetime.strptime(whois['expiration_date'], "%Y-%m-%d").date()
                else:
                    data['last_expiration_date'] = None

            if 'name_servers' not in domain_dict:
                data['name_servers'] = whois['name_servers']

            if 'registrar' not in domain_dict:
                data['registrar'] = whois['registrar']

        data['ssl_days_left'] = get_ssl_days_left(domain)
        data['ssl_error'] = get_ssl_error(domain)
        data['binom_allowed'] = get_binom_allowed(domain)

        return data

    except Exception as e:
        error_text = "Error: {}\n{}".format(str(e), traceback.format_exc())
        logging.error(error_text)

        return None
