from app.services import *
from bot.models import Bot_user, Referral


async def create_referral(bot_user: Bot_user, referrer: Bot_user):
    obj = await Referral.objects.acreate(
        bot_user=bot_user,
        referrer=referrer,
    )
    return obj


async def referrals_count_of_bot_user(bot_user: Bot_user, subscribed=False):
    if subscribed:
        count = await Referral.objects.filter(referrer__id=bot_user.id).exclude(
            subscription=None).acount()
    else:
        count = await Referral.objects.filter(referrer__id=bot_user.id).acount()
    return count
