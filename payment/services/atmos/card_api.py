from payment.services.atmos import *


async def bind_card_init_api(card_number: str, expiry: str) -> dict:
    """
    Пример ответа сервера:\n
    ```
    {
    "result": {
        "code": "OK",
        "description": "Нет ошибок"
    },
    "transaction_id": 442,
    "phone": "998900222222"
    }
    """
    data = {
        "card_number": card_number,
        "expiry": expiry
    }
    request = await EndpointRequest.create("partner/bind-card/init", data)
    response = await request.send()
    return response


async def bind_card_confirm_api(transaction_id, otp):
    """
    Пример ответа сервера:\n
    ```
    {
        "result": {
            "code": "OK",
            "description": "Нет ошибок"
        },
        "data": {
            "card_id": 1579076,
            "pan": "986009******1840",
            "expiry": "2505",
            "card_holder": "TEST",
            "balance": 1000000000,
            "phone": "998989999999",
            "card_token": "<card-token>"
        }
    }
    """
    data = {
        "transaction_id": transaction_id,
        "otp": otp
    }
    request = await EndpointRequest.create("partner/bind-card/confirm", data)
    response = await request.send()
    return response
