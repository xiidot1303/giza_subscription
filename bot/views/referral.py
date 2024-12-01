from app.views import *
from bot.bot import bot
from bot.services.referral_service import *
from app.services.subscription_service import *


async def main(request: HttpRequest, id):
    bot_user: Bot_user = await get_user_by_pk(id)
    async with bot:
        bot_username = bot.username
    if last_bonus_subscription := await get_last_bonus_subscription(bot_user):
        bonus_due_date = last_bonus_subscription.end_date.strftime("%d.%m.%Y")
    else:
        bonus_due_date = ""

    context = {
        "referral_link": f"https://t.me/{bot_username}?start=referrer--{bot_user.id}",
        "referrals_count": await referrals_count_of_bot_user(bot_user),
        "subscribed_referrals_count": await referrals_count_of_bot_user(bot_user, subscribed=True),
        "bonus_due_date": bonus_due_date,
    }
    return render(request, "referral/main.html", context=context)
