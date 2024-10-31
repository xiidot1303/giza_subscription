from app.services import *
from payment.models import Card
from bot.models import Bot_user


async def update_card_of_bot_user(bot_user: Bot_user, card_info: DictToClass):
    card, created = await Card.objects.aget_or_create(
        bot_user=bot_user,
    )
    card.number = card_info.number
    card.expire = card_info.expire
    card.token = card_info.token
    await card.asave()
    return card

async def get_card_of_bot_user(bot_user: Bot_user) -> Card:
    obj = await Card.objects.aget(bot_user__id = bot_user.id)
    return obj

async def update_card(card: Card, number, expire, token):
    card.number = number
    card.expire = expire
    card.token = token
    await card.asave()
    