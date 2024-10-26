from app.views import *
from app.services.plan_service import *
from payment.services.payme.subscribe_api import *
from config import PAYME_CHECKOUT_URL
from adrf.views import APIView
from adrf.requests import AsyncRequest
from config import DEBUG


async def set_card(request: HttpRequest):
    context = {
        "api_host": request.build_absolute_uri('/'),
        "debug": DEBUG
    }
    return render(request, 'subscribe/set_card.html', context=context)


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
