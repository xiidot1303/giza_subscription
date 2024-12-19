from app.services import *
from payment.models import Card
from bot.models import Bot_user
from payment.services.atmos import CardData as _CardInfo


async def update_card_of_bot_user(bot_user: Bot_user, card_info: _CardInfo):
    card, created = await Card.objects.aget_or_create(
        bot_user=bot_user,
    )
    card.number = card_info.pan
    card.expire = card_info.expiry
    card.token = card_info.card_token
    card.card_id = card_info.card_id
    card.holder = card_info.card_holder
    await card.asave()
    return card


async def get_card_of_bot_user(bot_user: Bot_user) -> Card:
    if obj := await Card.objects.filter(bot_user__id=bot_user.id).afirst():
        return obj
    else:
        obj = Card(
            number="----------------",
            expire="----",
            holder=""
        )
        return obj


async def delete_card_of_bot_user(bot_user: Bot_user):
    obj = await Card.objects.aget(bot_user__id=bot_user.id)
    await obj.adelete()
