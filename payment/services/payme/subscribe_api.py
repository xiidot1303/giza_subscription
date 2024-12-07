from payment.services.payme import *
from app.utils import DictToClass


async def cards_create_api(number, expire):
    """
    Response could be like this:\n
    {
        "jsonrpc": "2.0",
        "id": 123,
        "result": {
            "card": {
                "number": "860006******6311",
                "expire": "03/99",
                "token": "NTg0YTg0ZDYyYWJiNWNhYTMxMDc5OT...",
                "recurrent": true,
                "verify": false
            }
        }
    }
    """
    method = "cards.create"
    params = {
        "card": {
            "number": number,
            "expire": expire
        },
        "save": True
    }
    checkout_request = await CheckoutEndpointRequest.create(
        method, params, RequestType.POST
    )

    response = await checkout_request.send()
    return response


async def cards_get_verify_code_api(token):
    """Sample response:\n
    {
        "jsonrpc": "2.0",
        "id": 123,
        "result": {
            "sent": true,
            "phone": "99890*****31",
            "wait": 60000
        }
    }
    """
    method = "cards.get_verify_code"
    params = {
        "token": token
    }
    checkout_request = await CheckoutEndpointRequest.create(
        method, params, RequestType.POST
    )
    response = await checkout_request.send()
    return response


async def cards_verify_api(token, code):
    """Sample response:\n
    {
      "jsonrpc": "2.0",
      "id": 123,
      "result": {
        "card": {
          "number": "860006******6311",
          "expire": "03/99",
          "token": "NTg0YTgxZWYyYWJiNWNhYTMxMDc5OTExX...",
          "recurrent": True,
          "verify": True
        }
      }
    }
    """
    method = "cards.verify"
    params = {
        "token": token,
        "code": code
    }
    checkout_request = await CheckoutEndpointRequest.create(
        method, params, RequestType.POST
    )
    response = await checkout_request.send()
    return response


async def cards_check_api(token) -> DictToClass:
    """
    `obj.to_dict`:
    {
        card: {
            number: String,
            expire: String,
            token: String,
            recurrent: Boolean,
            verify: Boolean
        }
    }
    """
    method = "cards.check"
    params = {
        "token": token
    }
    checkout_request = await CheckoutEndpointRequest.create(
        method, params, RequestType.POST
    )
    response = await checkout_request.send()
    result: DictToClass = response["result"]
    return result


async def receipts_create_api(payment_id, amount):
    """
    Response: `receipt ID`
    """
    method = "receipts.create"
    params = {
        "amount": amount * 100,
        "account": {
            "account_id": str(payment_id)
        }
    }
    checkout_request = await CheckoutEndpointRequest.create(
        method, params, RequestType.POST
    )
    response = await checkout_request.send()
    print(response)
    receipt_id = response['result']['receipt']['_id']
    return receipt_id


async def receipts_pay_api(receipt_id, token) -> dict:
    """
    If "result" is available in response, then request is successfully.
    Otherwise, "error" is in response. It means request is not successfully
    """
    method = "receipts.pay"
    params = {
        "id": receipt_id,
        "token": token
    }
    checkout_request = await CheckoutEndpointRequest.create(
        method, params, RequestType.POST
    )
    response = await checkout_request.send()
    return response