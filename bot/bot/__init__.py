from telegram import Update, Message as BotMessage, MenuButtonWebApp, MenuButtonDefault
from telegram.ext import ContextTypes, CallbackContext, ExtBot, Application
from dataclasses import dataclass
from asgiref.sync import sync_to_async
from bot.utils import *
from bot.utils.bot_functions import *
from bot.utils.keyboards import *
from bot.resources.strings import lang_dict
from bot.services import *
from bot.services.language_service import *
from bot.services.string_service import *
from bot.services.text_service import *
from bot.resources.conversationList import *
from app.services import filter_objects_sync
from app.services.channel_access_service import has_channel_access
from app.services.setting_service import get_settings, Setting
from config import *


@dataclass
class WebhookUpdate:
    """Simple dataclass to wrap a custom update type"""
    user_id: int
    payload: str


class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):
    @classmethod
    def from_update(
        cls,
        update: object,
        application: "Application",
    ) -> "CustomContext":
        if isinstance(update, WebhookUpdate):
            return cls(application=application, user_id=update.user_id)
        return super().from_update(update, application)


async def main_menu(update: Update, context: CustomContext):
    bot_user: Bot_user = await get_object_by_update(update)
    # check that availablae channel access for this user
    if await has_channel_access(update.effective_user.id):
        # go to main menu
        text = await GetText.on(Text.main_menu)
        # add profile inline button
        i_open = InlineKeyboardButton(
            text=await get_word("open channel", update),
            url=TG_CHANNEL_INVITE_LINK
        )
        i_profile = InlineKeyboardButton(
            text=await get_word("profile", update),
            web_app=WebAppInfo(f"{WEBAPP_URL}/profile/{bot_user.id}")
        )

        # add referral inline button
        i_referral = InlineKeyboardButton(
            text=await get_word("referral", update),
            web_app=WebAppInfo(f"{WEBAPP_URL}/referral/{bot_user.id}")
        )
        buttons = [i_open, i_profile, i_referral]
        await context.bot.set_chat_menu_button(context._user_id, MenuButtonDefault())

    else:
        # go to start message
        text = await GetText.on(Text.start)
        i_join = InlineKeyboardButton(
            text=await get_word("join channel", update),
            url=TG_CHANNEL_INVITE_LINK
        )
        buttons = [i_join]

        # set referral page web app
        web_app_menu_button = MenuButtonWebApp(text="Referal",
                                               web_app=WebAppInfo(f"{WEBAPP_URL}/referral/{bot_user.id}"))
        await context.bot.set_chat_menu_button(context._user_id, web_app_menu_button)

    markup = InlineKeyboardMarkup([
        [button]
        for button in buttons
    ])
    await update_message_reply_text(update, text, reply_markup=markup)


async def is_message_back(update: Update):
    if update.message.text == await get_word("back", update):
        return True
    else:
        return False
