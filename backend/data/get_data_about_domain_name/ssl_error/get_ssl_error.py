import requests
import requests.exceptions


def get_ssl_error(domain):
    ssl_error = False
    try:
        requests.request("GET", 'https://' + domain)
    except:
        ssl_error = True

    return ssl_error
