import requests
import pyotp
import traceback
import logging
import json


def get_binom_response(binom, form):
    try:
        totp = pyotp.TOTP(binom["otp"])
        code2fa = totp.now()
        url = "{url}{form}&api_key={api}&code={code2fa}".format(url=binom['url_1'], api=binom['api'], code2fa=code2fa, form=form)
        payload = {}
        headers = {'Content-Type': 'application/json'}

        response = requests.request("GET", url, headers=headers, data=payload)

        return json.loads(response.text)

    except Exception as e:
        error_text = "Error: {}\n{}".format(str(e), traceback.format_exc())
        logging.error(error_text)
