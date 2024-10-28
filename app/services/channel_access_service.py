from app.services import *
from app.models import TelegramChannelAccess, Subscription
from bot.models import Bot_user


async def give_channel_access(bot_user: Bot_user, subscription: Subscription):
    obj = await TelegramChannelAccess.objects.acreate(
        bot_user=bot_user,
        subscription=subscription
    )
    return obj
