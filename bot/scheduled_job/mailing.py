from bot.models import Message, Bot_user
from app.models import TelegramChannelAccess, Subscription
from bot.utils.bot_functions import send_newsletter, bot
from bot.utils.keyboards import survey_options_keyboard
from asgiref.sync import async_to_sync
from django.db.models import Q


def send_message():
    for message in Message.objects.filter(is_sent=False):
        # save message as sent
        message.is_sent = True
        message.save()
        # get users
        if message.whom:
            active_bot_users_ids = TelegramChannelAccess.objects.filter().values_list(
                'bot_user__id', flat=True)
            subscribed_bot_users_ids = Subscription.objects.filter().values_list(
                'bot_user__id', flat=True).distinct()
            match message.whom:
                case "purchased":
                    users = Bot_user.objects.filter(id__in=active_bot_users_ids)
                case "did not extend":
                    users = Bot_user.objects.filter(
                        Q(id__in=subscribed_bot_users_ids) & ~Q(id__in=active_bot_users_ids)
                        )
                case "started and nothing":
                    users = Bot_user.objects.filter(
                        ~Q(id__in=subscribed_bot_users_ids)
                    )
        else:
            users = message.bot_users.all() or Bot_user.objects.all()
        for user in users:
            async_to_sync(send_newsletter)(
                bot, user.user_id, message.text,
                message.photo.open() if message.photo else None,
                message.video.open() if message.video else None,
                message.file.open() if message.file else None
            )


async def send_survey():
    # send survey to subscribers
    async for channel_access in TelegramChannelAccess.objects.all():
        bot_user: Bot_user = await channel_access.get_bot_user

        text = "Qaysi sohaga siz ko’proq e’tibor bermoqchisiz?"
        markup = await survey_options_keyboard()
        await send_newsletter(bot, bot_user.user_id, text, reply_markup=markup)