from app.views import *
from app.services.plan_service import *
from payment.services.payme.subscribe_api import *


async def set_card(request: HttpRequest):
    plan_id = request.GET.get('plan_id', None)
    plan: SubscriptionPlan = await get_subscription_plan_by_id(plan_id)
    return render(request, 'subscribe/set_card.html')


async def create_card(request: HttpRequest):
    # get data from POST
    number = request.POST.get('number')
    expire = request.POST.get('expire')

    # send request to payme endpoint to get token
    response = await cards_create_api(number, expire)
    
    return JsonResponse(response)

async def get_verify_code(request: HttpRequest):
    # get data from POST
    token = request.POST.get("token")

    # send verification
    response = await cards_get_verify_code(token)

    return JsonResponse(response)

async def verify(request: HttpRequest):
    # get data from POST
    token = request.POST.get("token")
    code = request.POST.get("code")

    # verify
    response = await cards_verify(token, code)
    return JsonResponse(response)
    