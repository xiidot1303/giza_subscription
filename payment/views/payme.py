from app.views import *
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from payment.resources.payme_responses import *
from payment.resources import payme_ips
from payment.utils import *
from payment.services.payme.merchant import *
from config import PAYME_KEY, PAYME_TEST_KEY

@csrf_exempt
def endpoint(request):
    try:
        # check request method
        if request.method == 'POST':
            error = None
            result = {}
            headers = request.headers
            data = json.loads(request.body.decode())
            id = data['id']
            auth = request.META["HTTP_AUTHORIZATION"]
            login, password = get_login_password_from_auth(auth)
            # check Authorization
            if (
                headers["X-Forwarded-For"] in payme_ips and
                login == 'Paycom'
            ):
                if password == PAYME_KEY:
                    test = False
                elif password == PAYME_TEST_KEY:
                    test = True
                else:
                    error = Errors.NOT_ENOUGH_PRIVILEGES
            else:
                error = Errors.NOT_ENOUGH_PRIVILEGES
            
            # BODY
            if not error:
                # get values
                method = data["method"]
                params = data["params"]
                # check method and create response
                if method == "CheckPerformTransaction":
                    amount, order_id = params["amount"], params["account"]["order_id"]
                    result, error = CheckPerformTransaction(amount, order_id)
                if method == "CreateTransaction":
                    payme_trans_id = params["id"]
                    time = params["time"]
                    amount = params["amount"]
                    order_id = params["account"]["order_id"]
                    result, error = CreateTransaction(payme_trans_id, time, amount, order_id, test)
                if method == "PerformTransaction":
                    payme_trans_id = params["id"]
                    result, error = PerformTransaction(payme_trans_id)
                if method == "CancelTransaction":
                    payme_trans_id = params["id"]
                    reason = params["reason"]
                    result, error = CancelTransaction(payme_trans_id ,reason)
                if method == "CheckTransaction":
                    payme_trans_id = params["id"]
                    result, error = CheckTransaction(payme_trans_id)
                if method == "GetStatement":
                    from_, to = params["from"], params["to"]
                    result, error = GetStatement(from_, to)



                # print(json.loads(request.body.decode()))
        else:
            error = Errors.REQUEST_IS_NOT_POST
    except Exception as ex:
        print(ex)
        error = Errors.NOT_ENOUGH_PRIVILEGES

    # CREATE RESPONSE
    response_data = {
        "jsonrpc": "2.0",
        "result": result,
        "id": id
    }
    if error:
        response_data = {
            "jsonrpc": "2.0",
            "id": id,
            "error": error,
        }

    response = JsonResponse(response_data)
    response['Content-Type'] = 'application/json'
    response['charset'] = 'UTF-8'
    return response

