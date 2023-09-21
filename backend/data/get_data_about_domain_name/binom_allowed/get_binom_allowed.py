import requests
from data.db.get_db_binoms import get_db_binoms


def get_binom_allowed(domain):
    binoms = get_db_binoms()

    binom_info = {}
    for binom in binoms:
        binom_name = binom["binom"]
        hash_value = binom["hash"]

        binom_info[binom_name] = hash_value

    reverse_binom_info = dict(zip(binom_info.values(), binom_info.keys()))

    try:
        responce = requests.get(f'https://{domain}/landers/unibi/')
        domain_hash = responce.text

        return reverse_binom_info.get(domain_hash, None)

    except:
        return None
