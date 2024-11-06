from bot.bot import *
from app.models import Subscription
from bot.services.string_service import *


async def your_subscription_changed_notify(
        user_id,
        old_subscription: Subscription, 
        new_subscription: Subscription
    ):

    expire_date = new_subscription.end_date.strftime("%d.%m.%Y")
    text = await your_subscription_changed_string(
        await old_subscription.get_plan_name,
        await new_subscription.get_plan_name,
        expire_date
    )
    await send_newsletter(bot, user_id, text)


async def deactivated_your_subscription_notify(user_id):
    text = await get_word('successfully deactivated subscription', chat_id=user_id)
    await send_newsletter(bot, user_id, text)