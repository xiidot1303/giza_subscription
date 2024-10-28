from app.services import *
from app.models import (
    TelegramChannelAccess,
    Subscription,
    Payment,
    SubscriptionPlan
)
from bot.models import Bot_user
from app.services.subscription_service import create_subscription as _create_subscription
from config import TG_CHANNEL_ID
from bot.bot import bot


async def give_channel_access(bot_user: Bot_user, subscription: Subscription):
    obj = await TelegramChannelAccess.objects.acreate(
        bot_user=bot_user,
        subscription=subscription
    )
    return obj


async def update_channel_access(subscription: Subscription, payment: Payment):
    bot_user: Bot_user = await subscription.get_bot_user
    plan: SubscriptionPlan = await subscription.get_plan

    # disactivate current subscription
    subscription.active = False
    await subscription.asave()

    # create new subscription
    await _create_subscription(bot_user, plan, payment)


async def remove_user_from_channel(subscription: Subscription):
    bot_user = await subscription.get_bot_user
    forty_seconds_later_timestamp = (await datetime_now() + timedelta(seconds=40)).timestamp()
    # kick user from channel without banning
    is_user_banned: bool = await bot.unban_chat_member(
        chat_id=TG_CHANNEL_ID,
        user_id=bot_user.user_id,
    )
    if is_user_banned:
        # get channel access objects
        channel_access = await TelegramChannelAccess.objects.aget(
            bot_user=bot_user)
        # delete channel access
        await channel_access.adelete()

        # deactivate subscription
        subscription.active = False
        await subscription.asave()