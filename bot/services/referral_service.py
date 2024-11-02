from app.services import *
from bot.models import Bot_user, Referral


async def create_referral(bot_user: Bot_user, referrer: Bot_user):
    obj = await Referral.objects.aget(
        bot_user = bot_user,
        referrer = referrer,
    )
    return obj