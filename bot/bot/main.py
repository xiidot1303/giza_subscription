from bot.bot import *
import json
import logging
import traceback
import html
from config import TG_CHANNEL_INVITE_LINK


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # create bot user if doesnt exist
    bot_user, created = await create_user_if_doesnt_exist(update.effective_user)
    bot_user: Bot_user

    # create inline button
    i_join = InlineKeyboardButton(
        text=await get_word("join channel", update),
        url=TG_CHANNEL_INVITE_LINK
    )
    buttons = [i_join]

    # check that availablae channel access for this user
    if await has_channel_access(update.effective_user.id):
        # go to main menu
        text = await GetText.on(Text.main_menu)
        # add profile inline button
        i_profile = InlineKeyboardButton(
            text=await get_word("profile", update),
            web_app=WebAppInfo(f"{WEBAPP_URL}/profile/{bot_user.id}")
        )
        buttons.append(i_profile)
    else:
        # go to start message
        text = await GetText.on(Text.start)

    markup = InlineKeyboardMarkup([
        [button]
        for button in buttons
    ])
    await update_message_reply_text(update, text, reply_markup=markup)


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
