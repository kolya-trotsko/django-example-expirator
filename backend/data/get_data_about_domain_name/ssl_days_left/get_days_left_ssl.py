import json
import traceback
import logging

def get_ssl_days_left(domain):
    from .infoSSLModule import SSLChecker
    try:
        ssl_checker = SSLChecker()
        args = {
            'hosts': [domain]
        }
        ssl_data = json.loads(ssl_checker.show_result(ssl_checker.get_args(json_args=args)))

        if domain in ssl_data:
            return str(ssl_data[domain]['valid_days_to_expire'])
        else:
            return None

    except Exception as e:
        error_text = "Error: {}\n{}".format(str(e), traceback.format_exc())
        logging.error(error_text)

        return None
