from app.views import *
from bot.services import *
from payment.services.card_service import *
from adrf.views import APIView
from adrf.requests import AsyncRequest


async def home(request: HttpRequest, id):
    # get bot user from their ID
    bot_user: Bot_user = await get_user_by_pk(id)
    # get card info of bot user
    card_info: Card = await get_card_of_bot_user(bot_user)
    context = {
        "card_number": card_info.number,
        "expire": card_info.expire,
        "api_host": request.build_absolute_uri('/'),
        "user_id": id
    }
    return render(request, "profile.html", context)


class UpdateCard(APIView):
    async def post(self, request: AsyncRequest, *args, **kwargs):
        # get data from data
        data = request.data
        card_number = data.get("card_number")
        expire = str(data.get("expire")).replace("/", "")
        token = data.get("token")
        user_id = data.get("user_id")
        
        bot_user: Bot_user = await get_user_by_pk(user_id)
        card: Card = await get_card_of_bot_user(bot_user)
        # update card data
        await update_card(card, card_number, expire, token)
        return JsonResponse({})