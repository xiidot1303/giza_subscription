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
    def __init__(self, method, params, type):
        self.request_method = method
        self.request_params = params
        self.request_type = type

        request_body = {
            "jsonrpc": "2.0",
            "id": async_to_sync(create_random_id)(),
            "method": self.request_method,
            "params": self.request_params
        }
        self.request_body = request_body

    async def send(self):
        response, header = await send_request(
            checkout_url, self.request_body, headers, self.request_type
        )
        return response
