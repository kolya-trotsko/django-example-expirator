import CloudFlare
import traceback
import logging
from data.db.get_db_cloudflares_acc import get_cloudflare_acc


def get_cloudflare_domains():
    cloudflares = get_cloudflare_acc()
    domains = {}

    for cloudflare in cloudflares:
        try:
            cf = CloudFlare.CloudFlare(email=cloudflare["email"], key=cloudflare["key"])
            zone = cf.zones.get()

            for domain in zone:
                try:
                    domains[domain['name']] = {
                        'cloudflare_acc': domain['account']['name'],
                        'name_servers': ", ".join(domain['name_servers'])
                    }

                except Exception as e:
                    error_text = "Error: {}\n{}".format(str(e), traceback.format_exc())
                    logging.error(error_text)

        except Exception as e:
            error_text = "Error: {}\n{}".format(str(e), traceback.format_exc())
            logging.error(error_text)

    return domains
