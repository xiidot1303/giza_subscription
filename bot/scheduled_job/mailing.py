from bot.models import Message, Bot_user
from bot.utils.bot_functions import send_newsletter, bot
from asgiref.sync import async_to_sync

def send_message():
    for message in Message.objects.filter(is_sent=False):
        # save message as sent
        message.is_sent = True
        message.save()
        # get users
        users = message.bot_users.all() or Bot_user.objects.all()
        for user in users:
            async_to_sync(send_newsletter)(
                bot, user.user_id, message.text, 
                message.photo.open() if message.photo else None, 
                message.video.open() if message.video else None, 
                message.file.open() if message.file else None
                )