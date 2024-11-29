from app.views import *
from app.services.plan_service import *
from app.services.setting_service import *
from payment.services.payme.subscribe_api import *
from payment.services.atmos.card_api import *
from config import PAYME_CHECKOUT_URL
from adrf.views import APIView
from adrf.requests import AsyncRequest
from config import DEBUG


async def set_card(request: HttpRequest):
    offer = await get_offer_url()
    support_url = await get_support_url()
    context = {
        "api_host": request.build_absolute_uri('/'),
        "debug": DEBUG,
        "offer_url": offer,
        "support_url": support_url
    }
    return render(request, 'subscribe/set_card.html', context=context)


# Atmos
class InitCardView(APIView):
    async def post(self, request: AsyncRequest, *args, **kwargs):
        # get data from POST
        number = request.data.get('number')
        expire = request.data.get('expire')
        expire = expire[2:] + expire[:2]
        # send request to payme endpoint to get token
        response = await bind_card_init_api(number, expire)
        return JsonResponse(response)


class CofirmCardView(APIView):
    async def post(self, request: AsyncRequest, *args, **kwargs):
        # get data from POST
        transaction_id = request.data.get("transaction_id")
        code = request.data.get("code")

        # confirm
        response = await bind_card_confirm_api(transaction_id, code)
        return JsonResponse(response)


# Payme
class CreateCardView(APIView):
    async def post(self, request: AsyncRequest, *args, **kwargs):
        # get data from POST
        number = request.data.get('number')
        expire = request.data.get('expire')
        # send request to payme endpoint to get token
        response = await cards_create_api(number, expire)
        return JsonResponse(response)


class GetVerifyCodeView(APIView):
    async def post(self, request: AsyncRequest, *args, **kwargs):
        # get data from POST
        token = request.data.get("token")

        # send verification
        response = await cards_get_verify_code_api(token)

        return JsonResponse(response)


class VerifyView(APIView):
    async def post(self, request: AsyncRequest, *args, **kwargs):
        # get data from POST
        token = request.data.get("token")
        code = request.data.get("code")

        # verify
        response = await cards_verify_api(token, code)
        return JsonResponse(response)
