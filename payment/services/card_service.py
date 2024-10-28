from app.services import *
from payment.models import Card
from bot.models import Bot_user


async def update_card_of_bot_user(bot_user: Bot_user, card_info: DictToClass):
    card, created = await Card.objects.aget_or_create(
        bot_user=bot_user,
    )
    card.number = card_info.number,
    card.expire = card_info.expire,
    card.token = card_info.token,
    await card.asave()
    return card
