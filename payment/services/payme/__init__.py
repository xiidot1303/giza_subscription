from config import *
from app.utils import send_request, create_random_id
from asgiref.sync import async_to_sync

checkout_url = PAYME_CHECKOUT_URL

headers = {
    'X-Auth': PAYME_TEST_XAUTH if DEBUG else f'{PAYME_CASH_ID}:{PAYME_KEY}',
    'Content-Type': 'application/json',
}


class RequestType:
    POST = 'post'
    GET = 'get'


class CheckoutEndpointRequest:
    def __init__(self, method, params, type, request_body):
        self.request_method = method
        self.request_params = params
        self.request_type = type
        self.request_body = request_body

    @classmethod
    async def create(cls, method, params, type):
        request_body = {
            "jsonrpc": "2.0",
            "id": await create_random_id(),
            "method": method,
            "params": params
        }
        instance = cls(method, params, type, request_body)
        return instance

    async def send(self):
        response, header = await send_request(
            checkout_url, self.request_body, headers, self.request_type
        )
        return response
