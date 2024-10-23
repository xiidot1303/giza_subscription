from bot.models import *
from bot.resources.strings import lang_dict
from telegram import Update

async def get_word(text, update: Update=None, chat_id=None):
    if not chat_id:
        chat_id = update.effective_user.id

    # this bot works only in uzbek
    # user = await Bot_user.objects.aget(user_id=chat_id)
    # if user.lang == "uz":
    #     result = lang_dict[text][0]
    # else:
    #     result = lang_dict[text][1]
    
    result = lang_dict[text][0]
    return result if result else text