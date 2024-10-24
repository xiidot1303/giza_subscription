import base64
import time

def get_login_password_from_auth(auth):
    basic, encoded_auth = auth.split(" ")
    login, password = str(base64.b64decode(encoded_auth).decode()).split(':')
    return login, password

def time_ts():
    return int(time.time()*1000)