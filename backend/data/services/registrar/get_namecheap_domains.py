import requests
import traceback
import datetime
import logging
import xmltodict
from data.db.get_db_registrars_acc import get_namecheap_acc
from time import sleep


def boolean(bool):
    if bool == 'false':
        return False
    elif bool == 'true':
        return True
    else:
        return None

def get_namecheap_response_domains_dict(namecheap):
    url = f"https://api.namecheap.com/xml.response?ApiUser={namecheap['api_user']}\
                        &ApiKey={namecheap['api_key']}\
                        &UserName={namecheap['api_user']}\
                        &Command=namecheap.domains.getList\
                        &ClientIp={namecheap['client_ip']}\
                        &PageSize=100"

    headers = {
        'Content-Type': 'application/json'
    }
    payload = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    result = xmltodict.parse(response.text)["ApiResponse"]["CommandResponse"]["DomainGetListResult"]["Domain"]

    return result


def get_namecheap_domains():
    try:
        namecheaps = get_namecheap_acc()
            
        domains = {}

        for namecheap in namecheaps:
            sleep(1)
            try:
                domains_dict = get_namecheap_response_domains_dict(namecheap)
                for domain in domains_dict:
                    domains[domain["@Name"]] = {
                                "last_expiration_date": datetime.datetime.strptime(domain["@Expires"], "%m/%d/%Y").date(),
                                "registrar": "Namecheap",
                                "registrar_acc": domain["@User"],
                                "auto_renew": boolean(domain["@AutoRenew"])
                                    }

            except Exception as e:
                error_text = "Error: {}\n{}".format(str(e), traceback.format_exc())
                logging.error(error_text)
        return domains

    except Exception as e:
        error_text = "Error: {}\n{}".format(str(e), traceback.format_exc())
        logging.error(error_text)
