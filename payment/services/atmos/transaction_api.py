from payment.services.atmos import *


async def create_transaction_api(account, amount):
    data = {
        "amount": amount * 100,
        "account": str(account),
        "store_id": ATMOS_STORE_ID,
    }
    request = await EndpointRequest.create('merchant/pay/create', data, RequestType.POST)
    response = await request.send()
    return response["transaction_id"]


async def pre_apply_transaction_api(transaction_id, card_token):
    """
    Sample response:
    ```
    {
        "result": {
            "code": "OK",
            "description": "Нет ошибок"
        }
    }
    """
    data = {
        "card_token": card_token,
        "store_id": ATMOS_STORE_ID,
        "transaction_id": transaction_id
    }
    request = await EndpointRequest.create('merchant/pay/pre-apply', data, RequestType.POST)
    response = await request.send()
    return response


async def apply_transaction_api(transaction_id):
    """
    Sample response:
    ```
    {
        "result": {
            "code": "OK",
            "description": "Нет ошибок"
        }
    }
    """
    data = {
        "transaction_id": transaction_id,
        "otp": 111111,
        "store_id": ATMOS_STORE_ID
    }
    request = await EndpointRequest.create('merchant/pay/apply-ofd', data, RequestType.POST)
    response = await request.send()
    return response
