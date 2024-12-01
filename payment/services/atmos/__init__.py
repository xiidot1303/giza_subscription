from config import (
    ATMOS_AUTHORIZATION_KEY,
    ATMOS_CONSUMER_KEY,
    ATMOS_CONSUMER_SECRET,
    ATMOS_STORE_ID
)
from app.utils import send_request, requests
from django.core.cache import cache
from asgiref.sync import async_to_sync
import base64

ATMOS_AUTHORIZATION_KEY = base64.b64encode(
    f"{ATMOS_CONSUMER_KEY}:{ATMOS_CONSUMER_SECRET}".encode("utf-8")
).decode("utf-8")


host = "https://partner.atmos.uz"


class RequestType:
    POST = 'post'
    GET = 'get'


class CardData:
    card_id: int
    pan: str
    expiry: str
    card_holder: str
    phone: str
    card_token: str


class EndpointRequest:
    def __init__(self, request_url, request_body, headers, type):
        self.request_url = request_url
        self.request_body = request_body
        self.request_type = type
        self.headers = headers

    @classmethod
    async def create(cls, url, params, type=RequestType.POST):
        request_url = f"{host}/{url}"
        if url == 'token':
            headers = {
                'Authorization': f"Basic {ATMOS_AUTHORIZATION_KEY}",
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            request_body = {"data": params}
        else:
            access_token = cache.get(
                "atmos:access_token") or await create_access_token()
            headers = {
                'Authorization': f"Bearer {access_token}",
                'Content-Type': 'application/json',
            }
            params['lang'] = 'uz'
            request_body = {"json": params}

        instance = cls(request_url, request_body, headers, type)
        return instance

    async def send(self):
        response = requests.post(
            self.request_url, **self.request_body, headers=self.headers)

        return response.json()


async def create_access_token():
    data = {
        "grant_type": "client_credentials"
    }
    request = await EndpointRequest.create('token', data, RequestType.POST)
    response = await request.send()
    try:
        access_token = response["access_token"]
        # set access token to redis
        await cache.aset("atmos:access_token", access_token, timeout=3600)
        await cache.aset("atmos:access_token:copy", access_token, timeout=5000)
        return access_token
    except Exception as ex:
        print(ex)
