from bot.models import *
from asgiref.sync import sync_to_async
from telegram import Update, User
from typing import Tuple

@sync_to_async
def is_registered(id):
    if Bot_user.objects.filter(user_id=id).exclude(phone=None):
        return True
    else:
        return False

async def get_user_by_update(update: Update):
    user = await Bot_user.objects.aget(user_id=update.effective_user.id)
    return user

async def check_username(update):
    user: Bot_user = await get_user_by_update(update)

    if user.username != update.message.chat.username:
        user.username = update.message.chat.username
        await user.asave()
    if user.firstname != update.message.chat.first_name:
        user.firstname = update.message.chat.first_name
        await user.asave()

async def get_or_create(user_id):
    obj = await Bot_user.objects.aget_or_create(user_id=user_id)
    
async def get_object_by_user_id(user_id):
    obj = await Bot_user.objects.aget(user_id=user_id)
    return obj

async def get_object_by_update(update: Update) -> Bot_user | None:
    obj = await Bot_user.objects.filter(user_id=update.effective_user.id).afirst()
    return obj

async def create_user_if_doesnt_exist(user: User) -> Tuple[Bot_user, bool]:
    obj, created = await Bot_user.objects.aget_or_create(
        user_id=user.id,
        defaults={
            "name": user.first_name,
            "firstname": user.first_name,
            "lang": "uz",
        }
    )
    return obj, created