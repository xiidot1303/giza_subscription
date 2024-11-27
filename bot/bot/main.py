from bot.bot import *
import json
import logging
import traceback
import html
from config import TG_CHANNEL_INVITE_LINK
from bot.services.referral_service import *
from bot.bot.login import _to_the_getting_name


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # create bot user if doesnt exist
    bot_user, created = await create_user_if_doesnt_exist(update.effective_user)
    bot_user: Bot_user
    # get start message
    referrer_id = await get_start_msg(update.effective_message.text)
    if created:
        if referrer_id:
            # get referrer object
            if referrer := await get_object_by_pk(referrer_id):
                # create Referral
                await create_referral(bot_user, referrer)

        # redirect to login
        return await _to_the_getting_name(update, context)

    await main_menu(update, context)

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
