from app.services import *
from app.models import (
    TelegramChannelAccess,
    Subscription,
    Payment,
    SubscriptionPlan
)
from bot.models import Bot_user
from app.services.subscription_service import (
    create_subscription as _create_subscription,
    get_subscription_by_id as _get_subscription_by_id,
    get_next_active_subscription as _get_next_active_subscription
)
from config import TG_CHANNEL_ID
from bot.utils.bot_functions import bot
from typing import Tuple


async def get_channel_access_of_bot_user(bot_user: Bot_user):
    obj = await TelegramChannelAccess.objects.filter(
        bot_user__id=bot_user.id).afirst()
    return obj


async def give_channel_access(bot_user: Bot_user, subscription: Subscription) -> Tuple[TelegramChannelAccess, bool]:
    """
    Return: (<`TelegramchannelAccess` objects>, <`is created` boolen>)
    """
    obj, created = await TelegramChannelAccess.objects.aget_or_create(
        bot_user=bot_user,
        defaults={
            "subscription": subscription
        }
    )
    return obj, created


async def update_channel_access(old_subscription: Subscription, new_subscription: Subscription):
    bot_user: Bot_user = await old_subscription.get_bot_user
    # disactivate current subscription
    old_subscription.active = False
    await old_subscription.asave()

    # get telegram channel access
    channel_access: TelegramChannelAccess = await TelegramChannelAccess.objects.aget(
        subscription=old_subscription)

    # set new subscription to channel access
    channel_access.subscription = new_subscription
    await channel_access.asave()


async def remove_user_from_channel(subscription: Subscription):
    bot_user = await subscription.get_bot_user
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


async def has_channel_access(user_id: int | str) -> bool:
    exists = await TelegramChannelAccess.objects.filter(
        bot_user__user_id=user_id
    ).aexists()
    return exists