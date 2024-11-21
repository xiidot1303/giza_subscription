from app.views import *
from django.http.response import JsonResponse
from adrf.views import APIView
from adrf.requests import AsyncRequest
from rest_framework.response import Response
from payment.resources.atmos_responses import *
from payment.resources import atmos_ip
from payment.services import *
from payment.utils import *
from config import ATMOS_CONSUMER_KEY


class CallbackData(DictToClass):
    store_id: int
    transaction_id: int
    transaction_time: int
    amount: int
    invoice: str
    sign: str


class Endpoint(APIView):
    async def check_authorization(self):
        # check ip address
        assert self.IP == atmos_ip, ACCESS_DENIED
        # check sign
        data = self.data
        sign = await generate_sign_atmos(data.store_id, data.transaction_id,
                                         data.invoice, data.amount, ATMOS_CONSUMER_KEY)
        assert sign == self.data.sign, INVALID_SIGN

    async def body(self, request: AsyncRequest, *args, **kwargs):
        data: CallbackData = self.data
        # check invoice is available
        invoice = await get_account_by_id(data.invoice)
        assert invoice, INVOICE_NOT_FOUND

        # check amount of the invoice
        assert data.amount == invoice.amount, AMOUNT_NOT_SATISFIED

        # successfully request, change account status to payed
        await account_pay(invoice, "atmos")

    async def post(self, request: AsyncRequest, *args, **kwargs):
        try:
            # make ready
            self.data = CallbackData(request.data)
            self.IP = request.headers["X-Forwarded-For"]

            # check Authorization
            await self.check_authorization()

            # BODY
            await self.body()
            code, message = SUCCESS
            status = 1

        except Exception as ex:
            code, message = ex
            status = 0

        response = {
            "status": status,
            "message": message
        }
        return Response(response, status=code)
