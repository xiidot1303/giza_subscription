from bot.bot import *
import json
import logging
import traceback
import html
from config import TG_CHANNEL_INVITE_LINK
from bot.bot.login import _to_the_getting_contact


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_registered(context._user_id):
        # get start message
        start_msg = await get_start_msg(update.effective_message.text)
        # stop if start msg is not available
        if not start_msg:
            await update_message_reply_text(
                update, 
                "Botdan foydalanish uchun maxsus link orqali ro'yxatdan o'tishingiz kerak."
                )
            return

        context.user_data['start_msg'] = start_msg

        # send hello message with instruction button
        # i_button = InlineKeyboardButton(
        #     text=await get_word("instruction", update),
        #     callback_data="start_instruction"
        # )
        # markup = InlineKeyboardMarkup([[i_button]])
        return await _to_the_getting_contact(update)

    await main_menu(update, context)


async def start_instruction(update: Update, context: CustomContext):
    # await bot_edit_message_reply_markup(update, context)
    settings: Setting = await get_settings()
    markup = ReplyKeyboardMarkup([[await get_word("registration", update)]],
                                 resize_keyboard=True, one_time_keyboard=True)
    await context.bot.send_video(context._user_id, settings.instruction_video_note_id, reply_markup=markup)


async def get_video_note_id(update: Update, context: CustomContext):
    await update_message_reply_text(update, update.message.video_note.file_id)


async def get_video_id(update: Update, context: CustomContext):
    await update_message_reply_text(update, update.message.video.file_id)

######################################################################
######################################################################
######################################################################

logger = logging.getLogger(__name__)


async def error_handler(update: Update, context: CustomContext):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error("Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        "An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    await context.bot.send_message(
        chat_id=206261493, text=message, parse_mode=ParseMode.HTML
    )
