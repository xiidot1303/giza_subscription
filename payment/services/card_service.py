from app.services import *
from payment.models import Card
from bot.models import Bot_user


async def create_card(bot_user: Bot_user, card_info: dict):
    """
    card_info = {
        number: String,
        expire: String,
        token: String,
        recurrent: Boolean,
        verify: Boolean
    }
    """
    card = await Card.objects.acreate(
        bot_user=bot_user,
        number=card_info["number"],
        expire=card_info["expire"],
        tokent=card_info["token"],
    )
    return card
