import whois
import traceback
import logging


def get_whois(domain):
    result = {
        'expiration_date': None,
        'name_servers': None,
        'registrar': None
    }
    try:
        who = whois.query(domain=domain)

        try:
            result['expiration_date'] = who.expiration_date.strftime("%Y-%m-%d")
        except:
            pass
        try:
            result['name_servers'] = ', '.join(who.name_servers)
        except:
            pass
        try:
            result['registrar'] = who.registrar
        except:
            pass

    except whois.exceptions.WhoisCommandFailed or whois.exceptions.FailedParsingWhoisOutput:
        pass
    except Exception as e:
        error_text = "Error: {}\n{}".format(str(e), traceback.format_exc())
        logging.error(error_text)

    return result
