import traceback
import datetime
import logging
from godaddypy import Client, Account
from data.db.get_db_registrars_acc import get_godaddy_acc
from time import sleep


def get_godaddy_domains():
    godaddies = get_godaddy_acc()
    result = {}
    for godaddy in godaddies:
        sleep(2)
        try:
            my_acct = Account(api_key=godaddy["api_key"], api_secret=godaddy["api_secret"])
            client = Client(my_acct)
            domains = client.get_domains()
            for domain in domains:
                sleep(1)
                try:
                    data = client.get_domain_info(domain)

                    admin_data = data.get("contactAdmin")
                    result[domain] = {}

                    if admin_data is not None:
                        if admin_data.get("nameFirst", False) or admin_data.get("nameLast", False):
                            result[domain]["registrar_acc"] = admin_data.get("nameFirst", "") + " " + admin_data.get("nameLast", "")
                    else:
                        result[domain]["registrar_acc"] = None

                    result[domain]["last_expiration_date"] = datetime.datetime.strptime(data.get("expires")[:10], "%Y-%m-%d").date()
                    result[domain]["registrar"] = "GoDaddy.com, LLC"
                    result[domain]["auto_renew"] = data.get("renewAuto")

                except Exception as e:
                    error_text = "Error: {}\n{}".format(str(e), traceback.format_exc())
                    logging.error(error_text)
                    
        except Exception as e:
            error_text = "Error: {}\n{}".format(str(e), traceback.format_exc())
            logging.error(error_text)

    return result
