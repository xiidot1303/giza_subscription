import base64
import time
import hashlib


async def get_login_password_from_auth(auth):
    basic, encoded_auth = auth.split(" ")
    login, password = str(base64.b64decode(encoded_auth).decode()).split(':')
    return login, password


async def generate_sign_atmos(store_id, transaction_id, invoice,
                              amount, api_key):
    sign = hashlib.sha256(
        (store_id + transaction_id + invoice + amount + api_key).encode()
    ).hexdigest()
    return sign


async def time_ts():
    return int(time.time()*1000)
