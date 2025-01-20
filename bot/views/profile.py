from app.views import *
from bot.services import *
from bot.bot import *
from bot.utils.keyboards import cancel_subscription_keyboard
from payment.services.card_service import *
from app.services.channel_access_service import *
from app.services.subscription_service import *
from app.services.payment_service import *
from adrf.views import APIView
from adrf.requests import AsyncRequest


async def home(request: HttpRequest, id):
    # get bot user from their ID
    bot_user: Bot_user = await get_user_by_pk(id)
    # get card info of bot user
    card_info: Card = await get_card_of_bot_user(bot_user)
    # get channel access
    channel_access: TelegramChannelAccess = await get_channel_access_of_bot_user(bot_user)
    subscription: Subscription = await channel_access.get_subscription
    plan: SubscriptionPlan = await subscription.get_plan
    payments = await filter_payed_payments_by_bot_user_list(bot_user)
    context = {
        # Card info
        "card_number": card_info.number,
        "expire": card_info.expire[2:] + card_info.expire[:2],
        "card_holder": card_info.holder,
        "api_host": request.build_absolute_uri('/'),
        "user_id": id,
        "bot_user_id": bot_user.user_id,

        # Tariff info
        "tariff": plan,
        "subscription": subscription,

        # Payment info
        "payments": payments,

    }
    return render(request, "profile/main.html", context)


class UpdateCard(APIView):
    async def post(self, request: AsyncRequest, *args, **kwargs):
        # get data from data
        data = request.data

        user_id = data.get("user_id")
        card_data = data.get("card_data")

        bot_user: Bot_user = await get_user_by_pk(user_id)
        # update card data
        await update_card_of_bot_user(bot_user, DictToClass(card_data))
        return JsonResponse({})


class CancelSubscription(APIView):
    async def post(self, request: AsyncRequest, *args, **kwargs):
        # get data from POST
        subscription_id = request.data.get("subscription_id")
        bot_user_id = request.data.get("bot_user_id")

        # send newsletter to user about cancellation
        text = await get_word("confirm cancellation", chat_id=bot_user_id)
        markup = await cancel_subscription_keyboard(subscription_id)
        result = await send_newsletter(bot, bot_user_id, text, reply_markup=markup)
        if result:
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})