from payment.services.payme import *


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
    checkout_request = CheckoutEndpointRequest(
        method, params, RequestType.POST
    )

    response = await checkout_request.send()
    return response


async def cards_get_verify_code(token):
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
    checkout_request = CheckoutEndpointRequest(
        method, params, RequestType.POST
    )
    response = await checkout_request.send()
    return response


async def cards_verify(token, code):
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
    checkout_request = CheckoutEndpointRequest(
        method, params, RequestType.POST
    )
    response = await checkout_request.send()
    return response


async def create_receipt_api(order_id, amount):
    requestBody = {
        "jsonrpc": "2.0",
        "id": 1111111,
        "method": "receipts.create",
        "params": {
            "amount": amount * 100,
            "account": {
                "order_id": str(order_id)
            }
        }
    }
    response, h = await send_request(checkout_url, requestBody, headers, 'post')
    trans_id = response['result']['receipt']['_id']
    payment_url = f'https://payme.uz/checkout/{trans_id}'
    return payment_url
