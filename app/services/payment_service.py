from app.services import *
from bot.models import Bot_user
from app.models import Payment


async def create_payment(bot_user: Bot_user, amount):
    obj = await Payment.objects.acreate(
        bot_user=bot_user, amount=amount
    )
    return obj
