from app.services import *
from app.models import Survey
from bot.models import Bot_user


async def create_survey(bot_user: Bot_user, answer: str) -> Survey:
    obj = await Survey.objects.acreate(bot_user=bot_user, answer=answer)
    return obj